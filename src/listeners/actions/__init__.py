from slack_bolt import App
from .sample_action import sample_action_callback
from .attendence_poll import attendance_poll_callback


def register(app: App):
    app.action("sample_action_id")(sample_action_callback)
    app.action("attendance_poll")(attendance_poll_callback)
