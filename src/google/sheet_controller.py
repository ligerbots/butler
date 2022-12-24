import pygsheets
from pygsheets import DataRange, Cell

from typing import Optional, List, Dict
from datetime import datetime

from ..dataTypes.classes import MeetingTime, Attendance, AttendancePoll, UserCreate, UserReturn, User, ForecastJob

gc = pygsheets.authorize(service_file='config/secrets/g-service.json')
 

MEETINGS_TO_FORECAST_SHIFT = (-1, 2)

class AttendanceSheetController():
    def __init__(self):
        self.gc = pygsheets.authorize(service_file='config/secrets/g-service.json')
        self.sh = self.gc.open_by_key("1_RjQocIi4hCZOkZhzQhN-_3efjWivihcLK0ibF29y3Q")
        self.users_sheet = self.sh.worksheet_by_title('Users')
        self.attendance_sheet = self.sh.worksheet_by_title('Attendance')
        self.forecast_sheet = self.sh.worksheet_by_title('Forecast')
        self.meetings_sheet = self.sh.worksheet_by_title('Meetings')

    # Named Range in Google Sheets
    def get_dates(self)-> List[List[Cell]]:
        dates_range = self.meetings_sheet.get_named_range("Dates", )
        dates = dates_range.cells
        return dates

    def get_nearest_date(self, date: datetime = datetime.now()) -> Cell:
        time_format = "%m/%d/%Y %H:%M"
        dates = self.get_dates()
        for cell in dates[0]:
            if len(cell.value) == 0:
                break
            date_value = datetime.strptime(cell.value, time_format)
            if date_value > date:
                return cell
        return dates[-1]

    def get_upcoming_meetings(self, window: int, date: datetime = datetime.now()) -> List[Cell]:
        current_cell = self.get_nearest_date(date)
        return self.meetings_sheet.get_values((current_cell.col, current_cell.row), (current_cell.col + 1, current_cell.row+window), include_tailing_empty=False, returnas='cell')

    def get_user(self, user: UserCreate) -> Optional[UserReturn]:
        search = self.users_sheet.find(user.email)
        if len(search) != 0:
            row = search[0].row
            first = self.users_sheet.get_value((row, 2))
            last = self.users_sheet.get_value((row, 3))
            return UserReturn(user.email, row, first, last)
        # return self.users_sheet.find(user.email, in_column=1, matchEntireCell=True)
    
    def translate_meeting_date_column_to_other_sheets(self, date: datetime) -> Optional[int]:
        cell = self.meetings_sheet.find(date.strftime("%m/%-d/%Y %H:%M"))
        if len(cell) == 0:
            return None
        return cell[0].col + MEETINGS_TO_FORECAST_SHIFT[1]
    
    def get_forecast_entry(self, user: UserReturn, date: datetime) -> Optional[Cell]: 
        column = self.translate_meeting_date_column_to_other_sheets(date)
        if column == None:
            return None
        return self.forecast_sheet.cell((user.row, column))

    def get_user_attendances(self, user: UserReturn, date: datetime = datetime.now()) -> List:
        attendances = self.attendance_sheet.get_row(user.row, include_tailing_empty=False)[2:]
        return self.attendance_sheet.get_row(user.row, include_tailing_empty=False)[2:]
    
    def get_user_forecasts(self, user: UserReturn, date: datetime = datetime.now()) -> List:
        return self.forecast_sheet.get_row(user.row, include_tailing_empty=False)[2:]
    
    @staticmethod
    def meeting_cell_time_format(cell: Cell) -> datetime:
        time_format = "%m/%d/%Y %H:%M"
        return datetime.strptime(cell.value, time_format)
    
    @staticmethod
    def reverse_meeting_cell_time_format(date: datetime) -> str:
        time_format = "%m/%-d/%Y %H:%M"
        return date.strftime(time_format)
    
    def get_attendance_poll(self, user: UserReturn, window: int, date: datetime = datetime.now()) -> Optional[AttendancePoll]:
        user = self.get_user(user)
        if user is None:
            return None
        upcoming_meetings = self.get_upcoming_meetings(window, date)
        if len(upcoming_meetings[0]) <= window:
           return None
        
        first_column = upcoming_meetings[0][0].col + MEETINGS_TO_FORECAST_SHIFT[1]
        last_column = upcoming_meetings[0][-1].col + MEETINGS_TO_FORECAST_SHIFT[1]
        shifted_row = user.row + MEETINGS_TO_FORECAST_SHIFT[0]

        forecast_range = self.forecast_sheet.get_values((user.row, first_column), (user.row, last_column), include_tailing_empty=False, returnas='cell')
        print(forecast_range)

        attendances = []
        for i, _ in enumerate(forecast_range[0]):
            meetingTime = MeetingTime(self.meeting_cell_time_format(upcoming_meetings[0][i]), 
            self.meeting_cell_time_format(upcoming_meetings[1][i]))
            if forecast_range[0][i].value == "TRUE":
                attendance_state = True
            elif forecast_range[0][i].value == "FALSE":
                attendance_state = False
            else:
                attendance_state = False
            attendance = Attendance(meetingTime=meetingTime, attendance=attendance_state)
            attendances.append(attendance)

        return AttendancePoll(attendances, User(user.email, user.first, user.last))
        # for 
        # return self.get_user_forecasts(user, date)[0:3]
    
    def add_user(self, user: User) -> UserReturn:
        searched_user = self.get_user(user)
        if searched_user is None:
            self.users_sheet.append_table([user.email, user.first, user.last])
            return self.get_user(user)
        else:
            return searched_user

    def update_forecast(self, poll: AttendancePoll):
        user = self.add_user(poll.user) # add user if not exist
        # self.attendance_sheet.unlink()
        first_entry = self.get_forecast_entry(user, poll.attendances[0].meetingTime.start)
        starting_column = first_entry.col
        self.forecast_sheet.update_row(user.row, [attendance.attendance for attendance in poll.attendances], starting_column)
        return True
    
    def batch_update_forecast(self, jobs: Dict[User, ForecastJob]):
        # self.forecast_sheet.unlink()
        for user, job in jobs.items():
            column = job.starting_column
            print("Starting Column: ", column)
            for attendance in job.poll.attendances:
                print("Updating: ", (user.row, column), attendance.attendance)

                # self.forecast_sheet.update_value((user.row, column), attendance.attendance)
                # column += 1
            # update the cells with the values in the poll
            def value_format(value: bool) -> dict:
                return [{"userEnteredValue": {"boolValue": value }}]

            values = [value_format(attendance.attendance) for attendance in job.poll.attendances]
            print(values)
            custom_request = {
                        "updateCells": 
                            {
                                "rows": {
                                    "values": values
                                },
                                "range": {
                                    "sheetId": self.forecast_sheet.id,
                                    "startRowIndex": user.row - 1,
                                    "endRowIndex": user.row,
                                    "startColumnIndex": column - 1,
                                    "endColumnIndex": column - 1 + len(job.poll.attendances),
                                },
                                "fields": "userEnteredValue"
                            },
                    }
            

            self.sh.custom_request(custom_request, fields="replies")
        
        # self.forecast_sheet.link()
        return True