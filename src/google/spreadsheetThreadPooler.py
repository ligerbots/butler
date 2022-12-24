from multiprocessing import Queue, Process

from ..dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob
from datetime import datetime

from .sheet_controller import AttendanceSheetController

import sys
from typing import Dict


class SpreadsheetThreadPooler(Process):
    def __init__(self, queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.attendancePollController = AttendanceSheetController()
        print(args)

    def run(self):
        print("SpreadsheetThreadPooler started")
        while True:
            batch: Dict[User, ForecastJob] = {}

            for payload in iter(self.queue.get, None):
                print("CYCLE START")
                user = payload.user
                attendancePoll = payload.poll
                    
                # Check if user is not in batch
                if user not in batch:
                    # Check if user is in sheet
                    user = self.attendancePollController.add_user(payload.user)
                    print(f"User: {user}")
                    print("Getting forecast entry")
                    starting_column = self.attendancePollController.get_forecast_entry(user, attendancePoll.attendances[0].meetingTime.start).col
                    print("Finished getting forecast entry")

                    attendanceJob = ForecastJob(user=user, poll=attendancePoll, starting_column=starting_column)

                    # Add new user and their attendance job to batch
                    batch[user] = attendanceJob

                    print("Batch: ", batch, self.queue.qsize())

                    print("CYCLE END")
                
                # User is in batch
                # Overwrite their poll
                batch[user].poll = attendancePoll
                print("User already in batch, overwriting poll")
                print("CYCLE END")

                if self.queue.empty():
                    print("Queue is empty, breaking")
                    break
                
            print("Running batch update")
            self.attendancePollController.batch_update_forecast(batch)
            print("Batch update complete")
            print("Batch: ", batch, self.queue.qsize())
            print("Clearing batch")
            batch = [] # Clear batch
            print("Batch cleared")