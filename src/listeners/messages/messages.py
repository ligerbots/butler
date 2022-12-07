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

def attendancePoll(context: BoltContext, client: WebClient, say: Say, logger: Logger):
    try:
        blocks = [					{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hi!\n*Select the meetings you will attend:*"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "checkboxes",
					"options": [
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/1:\tMonday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "6:30 PM ➡ 9:30 PM"
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/2:\tTuesday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "6:30 PM ➡ 9:30 PM"
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/3:\tWednesday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "6:30 PM ➡ 9:30 PM"
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/4:\tThursday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "6:30 PM ➡ 9:30 PM"
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/5:\tFriday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "9 AM ➡ 1:30 PM"
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/6:\tSaturday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "9 AM ➡ 1:30 PM"
							},
							"value": "value-2"
						}
					],
					"action_id": "attendance_poll"
				}
			]
		}
	]
        say(blocks=blocks, text="Pick a date to remind you")
    except Exception as e:
        print(e)
    

