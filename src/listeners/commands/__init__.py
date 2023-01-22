from slack_bolt import App
from . import commands
from . import admin


def register(app: App):
    app.command("/chant")(commands.liger_chant)
    app.command("/admin_schedule_message_check")(admin.schedule_message_check)
    app.command("/admin_schedule_message")(admin.schedule_message)
    app.command("/admin_status")(admin.status)
