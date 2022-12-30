from .dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob
from .google.sheet_controller import AttendanceSheetController
from .processes.messenger import Messenger
from datetime import datetime

from pprint import pprint

Messenger().run()
# forecasts = AttendanceSheetController().get_all_forecasts()
# for forecast in forecasts.values():
#     print(forecast.attendances)