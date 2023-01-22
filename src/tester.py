from .google.sheet_controller import AttendanceSheetController

from .dataTypes.classes import (
    MeetingTime,
    Attendance,
    AttendancePoll,
    User,
    ForecastJob,
    UserCreate,
    UserReturn,
)
import datetime
from pprint import pprint

# print(AttendanceSheetController().get_upcoming_meetings(10))
# user = UserReturn("ky200617@gmail.com", 1, "Kevin", "Yang")
# print(AttendanceSheetController().get_attendance_poll(user, 2))
# # pprint(AttendanceSheetController().get_upcoming_week_meetings())
print(AttendanceSheetController().get_success(datetime.datetime.now()))
td = datetime.timedelta((12 - datetime.datetime.now().weekday()) % 7)
next_saturday = datetime.datetime.now() + td
AttendanceSheetController().set_success(next_saturday, True, True)
