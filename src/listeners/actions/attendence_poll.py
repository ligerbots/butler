from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from pprint import pprint

from ...dataTypes.classes import AttendancePoll

def attendance_poll_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        user = body['user']['id']
        email = client.users_profile_get(user=user)['profile']['email']
        state_key = next(iter(body["state"]["values"]))
        pprint(body)
        state = body["state"]["values"][state_key]["attendance_poll"]["selected_options"]
        print(state)
        AttendancePoll.reverse_slack_poll(state)
        # pprint(state)

    except Exception as e:
        print(e)