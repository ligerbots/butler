from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from pprint import pprint 

def attendance_poll_callback(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        pprint(body)
    except Exception as e:
        print(e)