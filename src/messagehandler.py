import time
from .dataTypes.classes import (
    MeetingTime,
    Attendance,
    AttendancePoll,
    User,
    ForecastJob,
)
from .google.sheet_controller import AttendanceSheetController
from .processes.messenger import Messenger
from .process import spreadsheetUpdateQueue
from datetime import datetime

from pprint import pprint

RUN_DAY = 5
RUN_HOUR = 14

while True:

    datetime_obj = datetime.today()
    day_of_week = datetime_obj.weekday()

    while not getSuccess():

        if day_of_week == RUN_DAY and datetime_obj.hour == RUN_HOUR:
            response = Messenger.run()
            if response == 0:
                setSuccess()
                print("EXTREME SUCCESS")
            elif response == 1:
                print("EXTREME FAILURE")
                quit()
            elif response == 2:
                print("NO MEETINGS LEFT")
                quit()

        time.sleep(10)

    time.sleep(10)


# forecasts = AttendanceSheetController().get_all_forecasts()
# for forecast in forecasts.values():
#     print(forecast.attendances)
