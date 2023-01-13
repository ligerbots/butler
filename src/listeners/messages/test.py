from ...dataTypes.classes import MeetingTime, Attendance, AttendancePoll
import datetime

meetingTime1 = MeetingTime(
    startTime=datetime(2022, 12, 1, 18, 30, 0), endTime=datetime(2022, 12, 1, 21, 0, 0)
)
meetingTime2 = MeetingTime(
    startTime=datetime(2022, 12, 2, 18, 30, 0), endTime=datetime(2022, 12, 2, 21, 0, 0)
)
meetingTime3 = MeetingTime(
    startTime=datetime(2022, 12, 3, 18, 30, 0), endTime=datetime(2022, 12, 3, 21, 0, 0)
)
meetingTime4 = MeetingTime(
    startTime=datetime(2022, 12, 4, 18, 30, 0), endTime=datetime(2022, 12, 4, 21, 0, 0)
)

attendance1 = Attendance(meetingTime=meetingTime1, attendance=True)
attendance2 = Attendance(meetingTime=meetingTime2, attendance=False)
attendance3 = Attendance(meetingTime=meetingTime3, attendance=True)

attendances = [attendance1, attendance2, attendance3]
attendancePoll = AttendancePoll(attendances=attendances)

print(attendancePoll.generate_slack_poll())
