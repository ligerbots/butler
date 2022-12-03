import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

# Create slack client
client = WebClient(token=SLACK_BOT_TOKEN)

try:
    response = client.chat_postMessage(
        channel='U01C6SLHP0C',
        text="Hello!")
    assert response["message"]["text"] == "Hello!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")