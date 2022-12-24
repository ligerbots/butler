from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass


class UserCreate:
    email: str

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"{self.email}"

    def __eq__(self, other):
        return self.email == other.email

    def __hash__(self):
        return hash(self.email)


class User(UserCreate):
    first: str
    last: str

    def __init__(self, email, first, last):
        self.email = email
        self.first = first
        self.last = last

    def __repr__(self):
        base = super().__repr__()
        return f"{base}: {self.first} {self.last}"


class UserReturn(User):
    row: int

    def __init__(self, email, row, first, last):
        self.email = email
        self.row = row
        self.first = first
        self.last = last

    def __repr__(self):
        base = super().__repr__()
        return f"{base}: {self.row}"


class MeetingTime:
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
        return f"{startTime} ➡ {endTime}"

    # Returns the date in the format "12/1\tMonday"
    def title(self) -> str:
        startDate = self.start.strftime("%m/%d")
        weekDay = self.start.strftime("%A")
        return f"{startDate}\t{weekDay}"

    # Returns the day of the week ("Monday", "Tuesday", etc.)
    def weekDay(self) -> str:
        return self.start.strftime("%A")

    def date(self) -> str:
        return self.start.strftime("%m/%d")


class Attendance:
    meetingTime: MeetingTime
    attendance: bool

    def __init__(self, meetingTime: MeetingTime, attendance: bool):
        self.meetingTime = meetingTime
        self.attendance = attendance

    def select(self, attendance: bool):
        self.attendance = attendance

    def __str__(self) -> str:
        return f"{self.meetingTime.title()}: {self.attendance}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Attendance):
            return self.meetingTime.start == __o.meetingTime.start
        return False

    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, Attendance):
            return self.meetingTime.start < __o.meetingTime.start
        return False

    def __hash__(self) -> int:
        return hash(self.meetingTime.start)


class AttendancePoll:
    attendances: List[Attendance]
    user: User

    def __init__(self, attendances: List[Attendance], user: User):
        self.attendances = attendances
        self.user = user

    def __str__(self) -> str:
        return f"{self.user}: {self.attendances}"

    @staticmethod
    def update_total(
        total: List[Attendance], updated: List[Attendance]
    ) -> List[Attendance]:
        set_attendances = set(updated) | set(
            total
        )  # Update takes precedence, so the state in updated will be used first
        attendances = list(set_attendances)
        attendances.sort()
        return attendances

    @staticmethod
    def reverse_slack_poll(body: Dict, state: bool) -> List[Attendance]:
        attendances = []
        for meetingTime in body:
            title = meetingTime["text"]["text"]
            raw_date = title.split("\t")[0]

            raw_times = meetingTime["description"]["text"].split("➡")
            start_time = raw_times[0].strip()
            end_time = raw_times[1].strip()

            start_time = datetime.strptime(
                f"{datetime.now().year}/{raw_date} {start_time}", "%Y/%m/%d %I:%M %p"
            )
            end_time = datetime.strptime(
                f"{datetime.now().year}/{raw_date} {end_time}", "%Y/%m/%d %I:%M %p"
            )

            attendance = Attendance(
                MeetingTime(start_time, end_time), state
            )  # If entry is in state, then it is True by Slack Default
            attendances.append(attendance)
        return attendances

    def generate_slack_poll(self) -> str:
        def generate_options(self) -> Dict[str, List]:
            options = []
            for attendance in self.attendances:
                options.append(
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": attendance.meetingTime.title(),
                        },
                        "description": {
                            "type": "mrkdwn",
                            "text": attendance.meetingTime.timeSlot(),
                        },
                        "value": attendance.meetingTime.date(),
                    }
                )
            return options

        def generate_initial_options(self) -> Optional[Dict[str, List]]:
            initial_options = []
            
            for attendance in self.attendances:
                if attendance.attendance:
                    initial_options.append(
                        {
                            "text": {
                                "type": "mrkdwn",
                                "text": attendance.meetingTime.title(),
                            },
                            "description": {
                                "type": "mrkdwn",
                                "text": attendance.meetingTime.timeSlot(),
                            },
                            "value": attendance.meetingTime.date(),
                        }
                    )
            if len(initial_options) == 0:
                return None

            return initial_options

        # def generate_confirm() -> Dict[str, List]:
        #     confirm = {
        #         "confirm": {
        #             "title": {
        #                 "type": "plain_text",
        #                 "text": "Are you sure?"
        #             },
        #             "text": {
        #                 "type": "mrkdwn",
        #                 "text": "You are about to submit your attendance for the selected days."
        #             },
        #             "confirm": {
        #                 "type": "plain_text",
        #                 "text": "Submit"
        #             },
        #             "deny": {
        #                 "type": "plain_text",
        #                 "text": "Cancel"
        #             }
        #         }
        #     }
        #     return confirm

        poll = {
            "type": "actions",
            "elements": [
                {
                    "action_id": "attendance_poll",
                    "type": "checkboxes",
                }
            ],
        }
        poll["elements"][0]["options"] = generate_options(self)
        initial_options = generate_initial_options(self)
        
        # Do not add initial options if there are none. Slack gets mad if you do.
        if initial_options is not None:
            poll["elements"][0]["initial_options"] = initial_options
        return poll


@dataclass
class ForecastPayload:
    poll: AttendancePoll
    user: User


@dataclass
class ForecastJob(ForecastPayload):
    user: UserReturn
    starting_column: int
