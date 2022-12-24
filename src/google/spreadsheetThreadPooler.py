from multiprocessing import Queue, Process

from ..dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, AttendanceJob
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
            for attendancePoll in iter(self.queue.get, None):
                user = self.attendancePollController.add_user(attendancePoll.user)
                print(user)
                starting_column = self.attendancePollController.get_attendance_entry(user, attendancePoll.attendances[0].meetingTime.start).col
                attendanceJob = AttendanceJob(user, starting_column, attendancePoll)
                batch.append(attendanceJob)
                print(batch)
                print(self.queue.qsize())
                if self.queue.qsize() == 0:
                    break
            print("Running batch update")
            self.attendancePollController.batch_update_attendance(batch)
            batch.clear()