from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from pprint import pprint

from typing import List

from ...google.sheet_controller import AttendanceSheetController
from ...dataTypes.classes import (
    AttendancePoll,
    Attendance,
    UserCreate,
    ForecastPayload,
    User,
)
from ...process import spreadsheetUpdateQueue

def attendance_poll_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        # Acknowledge the action; this is required by slack (https://slack.dev/bolt-python/concepts#acknowledge)
        ack()

        # Get user info
        user_id = body["user"]["id"]

        user_profile = client.users_profile_get(
            user=user_id
        )  # User profiles searchable by user id (https://api.slack.com/methods/users.profile.get)
        first = user_profile["profile"]["first_name"]
        last = user_profile["profile"]["last_name"]
        email = user_profile["profile"]["email"]

        # Get the state of the poll
        state_key = next(
            iter(body["state"]["values"])
        )  # For some reason, the state key is a random string, so we have to get it this way

        # Raw attendance is all the options in the poll. This does not give state information!
        raw_attendance = body["message"]["blocks"][1]["elements"][0]["options"]
        # Updated state are the options that the user currently has selected. Has state info!
        updated_state = body["state"]["values"][state_key]["attendance_poll"][
            "selected_options"
        ]

        # Create AttendancePoll objects for all the poll options
        total_attendance: List[Attendance] = AttendancePoll.reverse_slack_poll(
            raw_attendance, False
        )
        # Create AttendancePoll objects for the user's selected options
        updated_attendance: List[Attendance] = AttendancePoll.reverse_slack_poll(
            updated_state, True
        )
        # Merge updated attendance into total attendance. Updated attendance will overwrite total attendance since it has state info.
        changed_attendance: List[Attendance] = AttendancePoll.update_total(
            total_attendance, updated_attendance
        )

        # Send data to child process
        attendance_payload = ForecastPayload(
            poll=AttendancePoll(changed_attendance, UserCreate(email)),
            user=User(email, first, last),
        )
        spreadsheetUpdateQueue.put(attendance_payload)  # Put data into queue
        print("Sent data to child process: ", attendance_payload)

    except Exception as e:
        print(e)