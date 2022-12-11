from logging import Logger

from slack_bolt import BoltContext, Say
from slack_sdk import WebClient
from typing import Union
import re

from ...dataTypes.classes import MeetingTime, Attendance, AttendancePoll

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
    meetingTime1 = MeetingTime(startTime=datetime(2022, 12, 1, 18, 30, 0), endTime=datetime(2022, 12, 1, 21, 0, 0))
    meetingTime2 = MeetingTime(startTime=datetime(2022, 12, 2, 18, 30, 0), endTime=datetime(2022, 12, 2, 21, 0, 0))
    meetingTime3 = MeetingTime(startTime=datetime(2022, 12, 3, 18, 30, 0), endTime=datetime(2022, 12, 3, 21, 0, 0))
    meetingTime4 = MeetingTime(startTime=datetime(2022, 12, 4, 18, 30, 0), endTime=datetime(2022, 12, 4, 21, 0, 0))

    attendance1 = Attendance(meetingTime=meetingTime1, attendance=True)
    attendance2 = Attendance(meetingTime=meetingTime2, attendance=False)
    attendance3 = Attendance(meetingTime=meetingTime3, attendance=True)

    attendances = [attendance1, attendance2, attendance3]
    attendancePoll = AttendancePoll(attendances=attendances)
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