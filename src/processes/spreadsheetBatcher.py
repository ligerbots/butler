from multiprocessing import Queue, Process
from ..dataTypes.classes import User, ForecastJob
from ..google.sheet_controller import AttendanceSheetController
from typing import Dict


class SpreadsheetBatcher(Process):
    def __init__(self, queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.attendancePollController = AttendanceSheetController()

    def run(self):
        print("Spreadsheet Thread Pooler Started")
        while True:
            updateBatch: Dict[User, ForecastJob] = {}

            # Go through all jobs in queue
            for payload in iter(self.queue.get, None):
                # Note that self.queue.get() consumes queue items

                # Rename payload components
                user = payload.user
                attendancePoll = payload.poll

                # Check if user is not in batch
                if user not in updateBatch:

                    # Check if user is in sheet
                    user = self.attendancePollController.lookup_or_add_user(
                        payload.user
                    )
                    # If the user is not in the sheet, add_user will auto add them.

                    # Grab the starting column based off of the first date in AttendancePoll
                    # Note: AttendancePoll is sorted by date (earliest to latest)

                    starting_column = self.attendancePollController.get_forecast_entry(
                        user, attendancePoll.attendances[0].meetingTime.start
                    )
                    if starting_column is None:
                        raise Exception(
                            f"Could not find starting column for user {user} and date {attendancePoll.attendances[0].meetingTime.start}"
                        )
                    starting_column = starting_column.col

                    # Construct ForecastJob to be used by batch update
                    attendanceJob = ForecastJob(
                        user=user, poll=attendancePoll, starting_column=starting_column
                    )

                    # Add new user and their attendance job to batch
                    updateBatch[user] = attendanceJob

                # If user is in batch, overwrite their poll
                updateBatch[user].poll = attendancePoll

                # Exit out if queue is empty
                if self.queue.empty():
                    break

            # When queue is empty, submit all changes to sheets
            self.attendancePollController.batch_update_forecast(updateBatch)

            # Clear batch
            updateBatch = []
