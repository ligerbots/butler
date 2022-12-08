from datetime import datetime
from typing import List

class MeetingTime():
    start: datetime
    end: datetime

    def __init__(self, startTime: datetime, endTime: datetime):
        self.start = startTime
        self.end = endTime
    
    # Returns the time slot in the format "6:30 PM ➡  9:00 PM"
    def timeSlot(self) -> str:
        TIME_SLOT_FORMAT = "%I:%M %p"
        startTime = self.start.strftime(TIME_SLOT_FORMAT)
        endTime = self.end.strftime(TIME_SLOT_FORMAT)
        return f"{startTime} ➡  {endTime}"

    # Returns the date in the format "12/1\tMonday"
    def date(self) -> str:
        startDate = self.start.strftime("%m/%d")
        weekDay = self.start.strftime("%A")
        return f"{startDate}\t{weekDay}"
    
    # Returns the day of the week ("Monday", "Tuesday", etc.)
    def weekDay(self) -> str:
        return self.start.strftime("%A")

class Attendance():
    meetingTime: MeetingTime
    attendance: bool

    def __init__(self, meetingTime: MeetingTime, attendance: bool):
        self.meetingTime = meetingTime
        self.attendance = attendance
    
    def select(self, attendance: bool):
        self.attendance = attendance

class AttendancePoll():
    attendances: List[Attendance]

    def __init__(self, attendances: List[Attendance]):
        self.attendances = attendances

    def generate_slack_poll(self) -> str:
        def generate_options(self) -> str:
            options = """
                        "options": [
            """
            for attendance in self.attendances:
                options += f"""
                            {{
                                "text": {{
                                    "type": "mrkdwn",
                                    "text": "{attendance.meetingTime.date()}"
                                }},
                                "description": {{
                                    "type": "mrkdwn",
                                    "text": "{attendance.meetingTime.timeSlot()}"
                                }},
                                "value": "{attendance.meetingTime.weekDay()}"
                            }},
                                """
            options = options[:-1]
            options += """
                        ],
                        """
            return options

        def generate_initial_options(self) -> str:
            initial_options = """
                                    "initial_options": [
            """
            for attendance in self.attendances:
                if attendance.attendance:
                    initial_options += f"""
                                            {{
                                                "text": {{
                                                    "type": "mrkdwn",
                                                    "text": "{attendance.meetingTime.date()}"
                                                }},
                                                "description": {{
                                                    "type": "mrkdwn",
                                                    "text": "{attendance.meetingTime.timeSlot()}"
                                                }},
                                                "value": "{attendance.meetingTime.weekDay()}"
                                            }},
                                            """
            initial_options = initial_options[:-1]
            initial_options += """
                                    ],
                                    """
            return initial_options
        
        def generate_confirm() -> str:
            confirm = """
                        "confirm": {
                            "title": {
                                "type": "plain_text",
                                "text": "Are you sure?"
                            },
                            "text": {
                                "type": "mrkdwn",
                                "text": "You are about to submit your attendance for the selected days."
                            },
                            "confirm": {
                                "type": "plain_text",
                                "text": "Submit"
                            },
                            "deny": {
                                "type": "plain_text",
                                "text": "Cancel"
                            }
                        }
                        """
            return confirm

        poll = """{
                            "type:" "actions",
                            "elements": [
                                {
                                    "action_id": "attendance_poll",
                                    "type": "checkboxes",
                            """
        poll += generate_options(self)
        poll += generate_initial_options(self)
        poll += """
                }
            ]
        }
                """


        return poll
        

if __name__ == "__main__":
    meetingTime1 = MeetingTime(startTime=datetime(2022, 12, 1, 18, 30, 0), endTime=datetime(2022, 12, 1, 21, 0, 0))
    meetingTime2 = MeetingTime(startTime=datetime(2022, 12, 2, 18, 30, 0), endTime=datetime(2022, 12, 2, 21, 0, 0))
    meetingTime3 = MeetingTime(startTime=datetime(2022, 12, 3, 18, 30, 0), endTime=datetime(2022, 12, 3, 21, 0, 0))
    meetingTime4 = MeetingTime(startTime=datetime(2022, 12, 4, 18, 30, 0), endTime=datetime(2022, 12, 4, 21, 0, 0))

    attendance1 = Attendance(meetingTime=meetingTime1, attendance=True)
    attendance2 = Attendance(meetingTime=meetingTime2, attendance=False)
    attendance3 = Attendance(meetingTime=meetingTime3, attendance=True)

    attendances = [attendance1, attendance2, attendance3]
    attendancePoll = AttendancePoll(attendances=attendances)
    print(attendancePoll.generate_slack_poll())

    
    