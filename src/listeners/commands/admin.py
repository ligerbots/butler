from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from ...utils.slack import admin_check
from ...dataTypes.classes import User

from datetime import datetime
import time

def status(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        if admin_check(ack, client, body, logger):
            client.chat_postEphemeral(
                channel=body["channel_id"],
                user=body["user_id"],
                text=f"Hi! You are an admin!"
            )
            return
        else:
            client.chat_postEphemeral(
                channel=body["channel_id"],
                user=body["user_id"],
                text=f"Hi! You are not an admin!"
            )
            return
    except Exception as e:
        logger.error(e)
    
def schedule_message_check(ack: Ack, client: WebClient, body: dict, logger: Logger):
    # try:
        ack()
        if not admin_check(ack, client, body, logger):
            return
        current = time.mktime(datetime.now().timetuple())

        results = client.chat_scheduledMessages_list(
            # oldest=current
        )

        print(results)
        
def schedule_message(ack: Ack, client: WebClient, body: dict, logger: Logger):
    try:
        ack()
        if not admin_check(ack, client, body, logger):
            return
        client.chat_scheduleMessage(
            channel=body["channel_id"],
            text="This is a scheduled message!",
            post_at=time.mktime(datetime.now().timetuple()) + 10
        )
    except Exception as e:
        logger.error(e)
    # except Exception as e:
    #     logger.error(e)