from multiprocessing import Process
from ..app import app
from slack_bolt import App

from typing import Dict
from ..google.sheet_controller import AttendanceSheetController
from ..dataTypes.classes import User, UserReturn

from datetime import datetime

import json
# Send slack messages to users when it is time for a meeting based off of the spreadsheet
# Send poll message every Sunday!
class Messenger(Process):
    def __init__(self):
        super().__init__()
        # self.messageQueue = messageQueue
        # self.logger = logger
        self.client = app.client
        self.sheetController = AttendanceSheetController()

    def sendPoll(self):
        def getMessageList():
            message_list_id = ""
            with open("config/slack_ids.json") as f:
                file = json.load(f)
                message_list_id = file["MESSAGE_LIST"]
            if message_list_id == "":
                raise Exception("Message List ID not found in config/slack_ids.json")
            
            message_list = self.client.usergroups_users_list(usergroup=message_list_id)
            print(message_list)
            if message_list["ok"] == False:
                raise Exception("Message List ID not found in config/slack_ids.json")
            return message_list["users"]

        user_ids = getMessageList()
        user_profiles = [self.client.users_profile_get(user = x)["profile"] for x in user_ids]
        print(user_profiles)
        
        # str being the user id
        users: Dict[UserReturn, str] = {}

        for i in range(len(user_profiles)):
            print(user_profiles[i])
            if "first_name" in user_profiles[i] and "last_name" in user_profiles[i]:
                first = user_profiles[i]["first_name"]
                last = user_profiles[i]["last_name"]
            else:
                try:
                    display_name = user_profiles[i]["display_name"]
                    split = display_name.split(" ")
                    first = split[0]
                    last = split[1]
                except:
                    first = "NO FIRST NAME GIVEN"
            
            email = user_profiles[i]["email"]
            id = user_ids[i]

            print(f"First: {first}, Last: {last}, Email: {email}")
            user = User(email=email, first=first, last=last)
            print("User is:", user)
            if user.email == None:
                raise Exception("User email is None")
            result = self.sheetController.get_user(user)
            print("Result is:", result)
            if result == None:
                result = self.sheetController.add_user(user)
                greeting = f"Hi {str(first)}! Welcome to the LigerBot! You've been added to the automatic attendance and forecast system! From now on, I'll be sending you forecasts every Saturday morning, and attendance polls 15 minutes before every meeting."
                print(greeting)
                self.client.chat_postMessage(channel=id, text=greeting)
            users[user] = id

        print(users)
        forecasts = self.sheetController.get_all_forecasts(window=4, date=datetime.now())

        print("Entering forecast sending loop")
        for user in users:
            forecast = forecasts[user]
            print(f"Sending forecast to {user.email}")
            id = users[user]
            json_poll = forecast.generate_slack_poll()
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hi! Here is this week's forecast poll.\n*Select the meetings you plan on attending:*"
                    }
                },
                json_poll
            ]
            
            self.client.chat_postMessage(channel=id, blocks=blocks, text="Hi! I was wondering if you could fill out this forecast poll for me? Thanks!")

            # self.client.chat_postMessage(channel=forecast.user.email, text=f"Hi {forecast.user.first}! Here's your forecast for the next 4 weeks: {forecast.forecast}")

    def run(self):
        # self.client.chat_postMessage(channel="C04DJG9J86R", text="Starting Send Process!")
        self.sendPoll()
        # self.logger.info("Messenger Process Started")
        # while True: