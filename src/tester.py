from .dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob
from .google.sheet_controller import AttendanceSheetController

from datetime import datetime

new_user = User("kevin@beantownbash.org", "Kevin", "Yang")
AttendanceSheetController().batch_get_forecasts(None)