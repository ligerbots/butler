from .dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob
from .google.sheet_controller import AttendanceSheetController

from datetime import datetime

new_user = User("kevin@beantownbash.org", "Kevin", "Yang")
AttendanceSheetController().lookup_or_add_user(new_user)