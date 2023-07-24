import requests
import time
import re
from datetime import datetime, timezone
import creds

JELLYFIN_URL = creds.HOST
API_KEY = creds.TOKEN
IDLE_THRESHOLD = 1 * 60  # 30 minutes in seconds

# Get a list of all users with their last activity timestamp
def get_users_last_activity():
    headers = {'X-Emby-Token': API_KEY}
    response = requests.get(f'{JELLYFIN_URL}/emby/Users', headers=headers)
    users = response.json()
    users_last_activity = {}

    for user in users:
        last_activity = user.get('LastActivityDate', '') or user.get('LastLoginDate', '')
        users_last_activity[user['Id']] = last_activity

    return users_last_activity

# Log out a user session
def logout_user_session(session_id):
    headers = {'X-Emby-Token': API_KEY}
    response = requests.post(f'{JELLYFIN_URL}/emby/Sessions/Logout/{session_id}', headers=headers)

    if response.status_code == 204:
        print(f'Successfully logged out session: {session_id}')
    else:
        print(f'Failed to log out session: {session_id}')

# Log out all sessions of a user
def logout_user_sessions(user_id):
    headers = {'X-Emby-Token': API_KEY}
    response = requests.post(f'{JELLYFIN_URL}/emby/Sessions/Logout?userId={user_id}', headers=headers)

    if response.status_code == 204:
        print(f'Successfully logged out all sessions of user: {user_id}')
    else:
        print(f'Failed to log out all sessions of user: {user_id}')

# Log out idle user accounts
def logout_idle_users():
    users_last_activity = get_users_last_activity()
    current_time = time.time()

    for user_id, last_activity in users_last_activity.items():
        if last_activity:
            match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', last_activity)
            if match:
                timestamp_str = match.group(0)
                timestamp = time.mktime(time.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S'))
                idle_duration = current_time - timestamp

                if idle_duration > IDLE_THRESHOLD:
                    logout_user_sessions(user_id)

# Run the script
logout_idle_users()