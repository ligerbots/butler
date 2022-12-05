from logging import Logger

from slack_bolt import BoltContext, Say
from slack_sdk import WebClient
from typing import Union
import re

def sayBots(context: BoltContext, client: WebClient, say: Say, logger: Logger):
    try:
        print(context)
        say("BOTS!")
    except Exception as e:
        logger.error(e)