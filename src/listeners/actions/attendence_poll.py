from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from pprint import pprint

from typing import List

from ...google.sheet_controller import AttendanceSheetController
from ...dataTypes.classes import AttendancePoll, Attendance, UserCreate

from ...main import queue

def attendance_poll_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        raw_user = body['user']['id']
        email = client.users_profile_get(user=raw_user)['profile']['email']
        state_key = next(iter(body["state"]["values"]))
        # pprint(body)
        total_attendance = body["message"]["blocks"][1]["elements"][0]["options"]
        updated_state = body["state"]["values"][state_key]["attendance_poll"]["selected_options"]

        total_attendance: List[Attendance] = AttendancePoll.reverse_slack_poll(total_attendance, False)

        updated_attendance: List[Attendance] = AttendancePoll.reverse_slack_poll(updated_state, True)
        changed_attendance: List[Attendance] = AttendancePoll.update_total(total_attendance, updated_attendance)

        attendance_poll = AttendancePoll(changed_attendance, UserCreate(email))
        queue.put(attendance_poll)
        print("Sent data to child: ", attendance_poll)
        # print(f"Total Attendance: {total_attendance}")
        # print(f"Updated Attendance: {updated_attendance}")
        # print(f"Changed Attendance: {changed_attendance}")
        # attendance_sheet_controller = AttendanceSheetController()

        # user = attendance_sheet_controller.get_user(UserCreate(email))
        # attendance_sheet_controller.update_attendance(attendance_poll)
        

    except Exception as e:
        print(e)