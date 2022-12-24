from logging import Logger

from slack_bolt import BoltContext, Say
from slack_sdk import WebClient
from typing import Union
from ...google.sheet_controller import AttendanceSheetController

from ...dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User

from pprint import pprint

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
        say(blocks=blocks, text="Pick a date to remind you")
    except Exception as e:
        print(e)

def attendancePoll(context: BoltContext, client: WebClient, say: Say, logger: Logger):
    MEETING_WINDOW = 4 # Note: Number is inclusive (i.e. 4 means 5 meetings)
    
    slack_user = client.users_profile_get(user=context["user_id"])
    first = slack_user["profile"]["first_name"]
    last = slack_user["profile"]["last_name"]

    email = slack_user["profile"]["email"]
    user = User(email, first, last)

    spreadsheetController = AttendanceSheetController()
    spreadsheet_user = spreadsheetController.get_user(user)
    if spreadsheet_user is None:
        say("Added you to the attendance sheet")
        spreadsheet_user = spreadsheetController.lookup_or_add_user(user)

    attendancePoll = spreadsheetController.get_attendance_poll(spreadsheet_user, MEETING_WINDOW, datetime.now())
    print("Attendance Poll:", attendancePoll)
    if attendancePoll is None:
        say("No more meetings to attend! :tada:")
        return
    
    try:
        json_poll = attendancePoll.generate_slack_poll()
        blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hi!\n*Select the meetings you will attend:*"
                    }
                },
                json_poll
            ]
        print("--------------------")
        pprint(blocks)
        say(blocks=blocks, text="Pick a date to remind you")
    except Exception as e:
        print(e)