from slack_bolt import Ack, Respond
from logging import Logger


# Example Snippet: https://slack.dev/bolt-python/concepts#commands
def sample_command_callback(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        # You always have to acknowledge slack after a command
        # It's the law 😤!
        ack()
        respond(
            f"Responding to the sample command! Your command was: {command['text']}"
        )
    except Exception as e:
        logger.error(e)


def liger_chant(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        respond("LigerBots! LigerBots! LigerBots!")
    except Exception as e:
        logger.error(e)


def whoami(command, ack: Ack, respond: Respond, logger: Logger):
    try:
        ack()
        respond("")
    except Exception as e:
        logger.error(e)
