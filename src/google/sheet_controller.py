import pygsheets
from pygsheets import DataRange, Cell, GridRange

from typing import Optional, List, Dict
from datetime import datetime

from ..dataTypes.classes import (
    MeetingTime,
    Attendance,
    AttendancePoll,
    UserCreate,
    UserReturn,
    User,
    ForecastJob,
)

gc = pygsheets.authorize(service_file="config/secrets/g-service.json")


MEETINGS_TO_FORECAST_SHIFT = (-1, 2)
MEETING_TIME_FORMAT = "%m/%d/%Y %H:%M"
MEETING_TIME_FORMAT_NO_LEADING_ZERO = "%m/%-d/%Y %H:%M" # - removes the leading zero from the day

class AttendanceSheetController:
    def __init__(self):
        self.gc = pygsheets.authorize(service_file="config/secrets/g-service.json")
        self.sh = self.gc.open_by_key("1_RjQocIi4hCZOkZhzQhN-_3efjWivihcLK0ibF29y3Q")
        self.users_sheet = self.sh.worksheet_by_title("Users")
        self.attendance_sheet = self.sh.worksheet_by_title("Attendance")
        self.forecast_sheet = self.sh.worksheet_by_title("Forecast")
        self.meetings_sheet = self.sh.worksheet_by_title("Meetings")


    # Methods to convert the format of the time in the Meetings sheet to a datetime object
    @staticmethod
    def meeting_cell_time_format(cell: Cell) -> datetime:
        time_format = MEETING_TIME_FORMAT
        return datetime.strptime(cell.value, time_format)

    @staticmethod
    def reverse_meeting_cell_time_format(date: datetime) -> str:
        time_format = MEETING_TIME_FORMAT_NO_LEADING_ZERO
        return date.strftime(time_format)
    
    # Get dates from the Meetings sheet based off of the named range "Dates"
    # IMPORTANT TO REMEMBER THIS IN SETUP OF A NEW SHEET!
    def get_dates(self) -> List[List[Cell]]:
        dates_range = self.meetings_sheet.get_named_range(
            "Dates",
        )
        dates = dates_range.cells
        return dates

    # Get the nearest date to the current date
    def get_nearest_date(self, date: datetime = datetime.now()) -> Cell:
        dates = self.get_dates()
        for cell in dates[0]:
            if len(cell.value) == 0:
                break
            date_value = datetime.strptime(cell.value, MEETING_TIME_FORMAT)
            if date_value > date:
                return cell
        return dates[-1]

    def get_upcoming_meetings(
        self, window: int, date: datetime = datetime.now()
    ) -> List[Cell]:
        current_date_cell = self.get_nearest_date(date)
        remaining_meetings = self.meetings_sheet.get_values(
            (current_date_cell.row, current_date_cell.col),
            (current_date_cell.row + 1, current_date_cell.col + window),
            include_tailing_empty=False,
            returnas="cell",
        )
        return remaining_meetings

    def get_user(self, user: UserCreate) -> Optional[UserReturn]:
        search = self.users_sheet.find(user.email)
        if len(search) != 0:
            row = search[0].row
            first = self.users_sheet.get_value((row, 2))
            last = self.users_sheet.get_value((row, 3))
            return UserReturn(user.email, row, first, last)
        return None
        # return self.users_sheet.find(user.email, in_column=1, matchEntireCell=True)

    def translate_date_column(
        self, date: datetime
    ) -> Optional[int]:
        cell = self.meetings_sheet.find(date.strftime(MEETING_TIME_FORMAT_NO_LEADING_ZERO))
        if len(cell) == 0:
            return None
        return cell[0].col + MEETINGS_TO_FORECAST_SHIFT[1]

    def get_forecast_entry(self, user: UserReturn, date: datetime) -> Optional[Cell]:
        column = self.translate_date_column(date)
        if column == None:
            return None
        return self.forecast_sheet.cell((user.row, column))

    def get_user_attendances(
        self, user: UserReturn
    ) -> List:
        return self.attendance_sheet.get_row(user.row, include_tailing_empty=False)[2:]

    def get_user_forecasts(
        self, user: UserReturn
    ) -> List:
        return self.forecast_sheet.get_row(user.row, include_tailing_empty=False)[2:]

    def get_attendance_poll(
        self, user: UserReturn, window: int, date: datetime = datetime.now()
    ) -> Optional[AttendancePoll]:
        user = self.get_user(user)
        if user is None:
            return None
        upcoming_meetings = self.get_upcoming_meetings(window, date)
        if len(upcoming_meetings[0]) == 0:
            # No more meetings!
            return None

        print("Upcoming Meetings:   ", upcoming_meetings)
        # Hard coded optimization so we can avoid another search API Call (which is O(n))
        # Assumes that the meetings are sorted!
        first_column = upcoming_meetings[0][0].col + MEETINGS_TO_FORECAST_SHIFT[1] 
        last_column = upcoming_meetings[0][-1].col + MEETINGS_TO_FORECAST_SHIFT[1]

        forecast_range = self.forecast_sheet.get_values(
            (user.row, first_column),
            (user.row, last_column),
            include_tailing_empty=False,
            returnas="cell",
        )
        attendances = []
        for i in range(len(upcoming_meetings[0])):
            meetingTime = MeetingTime(
                self.meeting_cell_time_format(upcoming_meetings[0][i]),
                self.meeting_cell_time_format(upcoming_meetings[1][i]),
            )

            # Map spreadsheet values to python booleans
            attendance_state = True if forecast_range[0][i].value == "TRUE" else False
            
            attendance = Attendance(
                meetingTime=meetingTime, attendance=attendance_state
            )
            attendances.append(attendance)
        
        returnUser = User(user.email, user.first, user.last)
        attendancePoll = AttendancePoll(attendances, returnUser) 
        print(attendancePoll)
        print("HERE")
        return attendancePoll

    # Both checks for user and adds user if not exist
    def lookup_or_add_user(self, user: User) -> UserReturn:
        searched_user = self.get_user(user) # Check if user exists
        if searched_user is None:
            self.users_sheet.append_table([user.email, user.first, user.last]) # Add user to the end of the Users sheet
            return self.get_user(user)
        else:
            return searched_user

    ## Update the forecast sheet with the attendance poll
    ## THIS FUNCTION IS SOOOOOO SLOW. USE BATCH UPDATE FORECAST INSTEAD!!!
    # def update_forecast(self, poll: AttendancePoll):
    #     user = self.lookup_add_user(poll.user)  # Check if user exists, add them if not
    #     first_entry = self.get_forecast_entry(
    #         user, poll.attendances[0].meetingTime.start
    #     )
    #     starting_column = first_entry.col
    #     self.forecast_sheet.update_row(
    #         user.row,
    #         [attendance.attendance for attendance in poll.attendances],
    #         starting_column,
    #     )
    #     return True

    # Custom batch update for cells
    def batch_update_forecast(self, jobs: Dict[User, ForecastJob]):
        # Jobs will contain a dictionary of users and their forecast jobs
        for user, job in jobs.items():
            column = job.starting_column
    
            # Update the cells with the values in the poll
            def dynamic_value_format(value: bool) -> dict:
                return [{"userEnteredValue": {"boolValue": value}}]

            # Custom request to update cells based off (https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate)
            values = [
                dynamic_value_format(attendance.attendance)
                for attendance in job.poll.attendances
            ]

            # Note: The index is 0 based, so the first row is 0, the second row is 1, etc.
            # Thus we need to subtract 1 from the indexes
            custom_request = {
                "updateCells": {
                    "rows": {"values": values},
                    "range": {
                        "sheetId": self.forecast_sheet.id,
                        "startRowIndex": user.row - 1,
                        "endRowIndex": user.row,
                        "startColumnIndex": column - 1,
                        "endColumnIndex": column - 1 + len(job.poll.attendances),
                    },
                    "fields": "userEnteredValue",
                },
            }

            # Run the custom request
            self.sh.custom_request(custom_request, fields="replies")

        return True