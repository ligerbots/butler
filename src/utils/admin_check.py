import json
from ..dataTypes.classes import UserCreate

from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient
from ..dataTypes.classes import User

# def admin_check(user: UserCreate) -> bool:
#     """Check if user is admin"""

#     if user.email in config["ADMINS"]:
#         return True
#     else:
#         return False

def admin_check(ack: Ack, client: WebClient, body: dict, logger: Logger) -> bool:
    """Check if user is admin"""
    user_id = body["user_id"]
    user_profile = client.users_profile_get(user=user_id)["profile"]

    user = User(email=user_profile["email"], first=user_profile["first_name"], last=user_profile["last_name"])
    
    with open("config/slack_ids.json", "r") as f:
        slack_ids = json.load(f)
    
    admins = client.usergroups_users_list(usergroup=slack_ids["ADMIN_LIST"])["users"]

    if user_id in admins:
        return True
    return False