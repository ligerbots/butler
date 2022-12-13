from logging import Logger

from slack_bolt import BoltContext, Say
from slack_sdk import WebClient
from typing import Union
from ...google.sheets import AttendanceSheetController
import re

from ...dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User

from datetime import datetime

def sayBots(context: BoltContext, client: WebClient, say: Say, logger: Logger):
    try:
        print(context)
        say("BOTS!")
    except Exception as e:
        logger.error(e)

def attendancePollTest(context: BoltContext, client: WebClient, say: Say, logger: Logger):
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
					"action_id": "attendance_poll",
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
							"value": "Monday"
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
							"value": "Tuesday"
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
							"value": "Wednesday"
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
							"value": "Thursday"
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
							"value": "Friday"
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
							"value": "Saturday"
						}
					],
                    "initial_options": [
						{
							"text": {
								"type": "mrkdwn",
								"text": "12/6:\tSaturday"
							},
							"description": {
								"type": "mrkdwn",
								"text": "9 AM ➡ 1:30 PM"
							},
							"value": "Saturday"
						}
                    ]
				}
			]
		}
	]
        print(blocks)
        say(blocks=blocks, text="Pick a date to remind you")
    except Exception as e:
        print(e)

def attendancePoll(context: BoltContext, client: WebClient, say: Say, logger: Logger):
    MEETING_WINDOW = 4
    slack_user = client.users_profile_get(user=context["user_id"])
    name = slack_user["profile"]["real_name"]
    email = slack_user["profile"]["email"]
    user = User(email, name.split(" ")[0], name.split(" ")[1])
    spreadsheetController = AttendanceSheetController()
    spreadsheet_user = spreadsheetController.get_user(user)
    if spreadsheet_user is None:
        say("Added you to the attendance sheet")
        spreadsheet_user = spreadsheetController.add_user(user)

    attendancePoll = spreadsheetController.get_attendance_poll(spreadsheet_user, MEETING_WINDOW, datetime(2022, 12, 3)) 
    if attendancePoll is None:
        say("No more meetings to attend")
        return

    try:
        blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hi!\n*Select the meetings you will attend:*"
                    }
                },
                attendancePoll.generate_slack_poll()
            ]
        print(blocks)
        say(blocks=blocks, text="Pick a date to remind you")
    except Exception as e:
        print(e)