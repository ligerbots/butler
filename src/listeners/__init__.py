# from listeners import actions
from .  import actions
from .  import commands
from .  import events
from .  import messages
from .  import shortcuts
from .  import views

def register_listeners(app):
    actions.register(app)
    commands.register(app)
    events.register(app)
    messages.register(app)
    shortcuts.register(app)
    views.register(app)