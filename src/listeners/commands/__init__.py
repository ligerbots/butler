from slack_bolt import App
from . import commands

def register(app: App):
    app.command("/chant")(commands.liger_chant)