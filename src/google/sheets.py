import pygsheets
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

gc = pygsheets.authorize(service_file='config/secrets/g-service.json')
 
class UserCreate():
    email: str
    def __init__(self, email):
        self.email = email

class UserReturn(UserCreate):
    row: int
    first: str
    last: str
    def __init__(self, email, row, first, last):
        self.email = email
        self.row = row
        self.first = first
        self.last = last
    
    def __str__(self):
        return f"User {self.row}: {self.first} {self.last}"

class AttendanceSheet():
    def __init__(self):
        self.gc = pygsheets.authorize(service_file='config/secrets/g-service.json')
        self.sh = self.gc.open_by_key("1_RjQocIi4hCZOkZhzQhN-_3efjWivihcLK0ibF29y3Q")
        self.users_sheet = self.sh.worksheet_by_title('Users')
        self.attendance_sheet = self.sh.worksheet_by_title('Attendance')
        self.forecast_sheet = self.sh.worksheet_by_title('Forecast')
        self.meetings_sheet = self.sh.worksheet_by_title('Meetings')

    def get_dates(self):
        return self.meetings_sheet.get_row(1, include_tailing_empty=False)[1:]
    
    def get_user(self, user: UserCreate) -> Optional[UserReturn]:
        search = self.users_sheet.find(user.email)
        if len(search) != 0:
            row = search[0].row
            first = self.users_sheet.get_value((row, 2))
            last = self.users_sheet.get_value((row, 3))
            return UserReturn(user.email, row, first, last)
        # return self.users_sheet.find(user.email, in_column=1, matchEntireCell=True)
    
    def get_attendance(self, user: UserReturn, date: datetime):

    def get_user_attendances(self, user: UserReturn) -> List:
        return self.attendance_sheet.get_row(user.row, include_tailing_empty=False)[2:]
    
    def get_user_forecasts(self, user: UserReturn) -> List:
        return self.forecast_sheet.get_row(user.row, include_tailing_empty=False)[2:]
    
user1 = UserCreate(email="ky200617@gmail.com")
userR1 = AttendanceSheet().get_user(user1)
print(AttendanceSheet().get_dates())
print(AttendanceSheet().get_attendance(userR1))
print(AttendanceSheet().get_forecast(userR1))