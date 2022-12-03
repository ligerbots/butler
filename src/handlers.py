import os
from slack_sdk.scim  import SCIMClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

client = SCIMClient(token=SLACK_BOT_TOKEN)

def getUserGroups():
    try:
        response = client.search_groups(start_index=1, count=100)
        print(response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")

getUserGroups()