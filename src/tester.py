from .dataTypes.classes import MeetingTime, Attendance, AttendancePoll, User, ForecastJob
from .google.sheet_controller import AttendanceSheetController
from .processes.messenger import Messenger
from datetime import datetime

Messenger().run()