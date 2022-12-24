from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from pprint import pprint

from typing import List

from ...google.sheet_controller import AttendanceSheetController
from ...dataTypes.classes import AttendancePoll, Attendance, UserCreate, ForecastPayload, User
from ...main import queue

def attendance_poll_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        user_id = body['user']['id']

        user_profile = client.users_profile_get(user=user_id)
        first = user_profile['profile']['first_name']
        last = user_profile['profile']['last_name']
        email = user_profile['profile']['email']

        state_key = next(iter(body["state"]["values"]))
        raw_attendance = body["message"]["blocks"][1]["elements"][0]["options"]
        updated_state = body["state"]["values"][state_key]["attendance_poll"]["selected_options"]

        total_attendance: List[Attendance] = AttendancePoll.reverse_slack_poll(raw_attendance, False)
        updated_attendance: List[Attendance] = AttendancePoll.reverse_slack_poll(updated_state, True)
        changed_attendance: List[Attendance] = AttendancePoll.update_total(total_attendance, updated_attendance)

        attendance_payload = ForecastPayload(poll=AttendancePoll(changed_attendance, UserCreate(email)), user = User(email, first, last))
        queue.put(attendance_payload)
        print("Sent data to child process: ", attendance_payload)

    except Exception as e:
        print(e)