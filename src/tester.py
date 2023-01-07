from .google.sheet_controller import AttendanceSheetController

from .dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob, UserCreate, UserReturn
from pprint import pprint

print(AttendanceSheetController().get_upcoming_meetings(10))
user = UserReturn("ky200617@gmail.com", 1, "Kevin", "Yang")
print(AttendanceSheetController().get_attendance_poll(user, 2))
# pprint(AttendanceSheetController().get_upcoming_week_meetings())