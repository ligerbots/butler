from multiprocessing import Queue, Process

from ..dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob
from datetime import datetime

from .sheet_controller import AttendanceSheetController

import sys


class SpreadsheetThreadPooler(Process):
    def __init__(self, queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.attendancePollController = AttendanceSheetController()
        print(args)

    def run(self):
        print("SpreadsheetThreadPooler started")
        while True:
            batch = []
            for payload in iter(self.queue.get, None):
                attendancePoll = payload.poll
                user = self.attendancePollController.add_user(payload.user)
                print(f"User: {user}")
                starting_column = self.attendancePollController.get_forecast_entry(user, attendancePoll.attendances[0].meetingTime.start).col
                attendanceJob = ForecastJob(user, starting_column, attendancePoll)
                batch.append(attendanceJob)
                print("Batch: ", batch, self.queue.qsize())
                if self.queue.qsize() == 0:
                    break
            print("Running batch update")
            self.attendancePollController.batch_update_forecast(batch)
            batch.clear()