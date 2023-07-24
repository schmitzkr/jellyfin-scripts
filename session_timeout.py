"""end idle sessions on jellyfin instance"""
#!/usr/bin/env python

from datetime import datetime, timezone
from datetime import timedelta
from dateutil import parser
import requests
import creds

headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
    'Authorization': 'MediaBrowser Token="' + creds.TOKEN + '"'
}
print (headers)
URL = creds.HOST

def get_last_activity():
    """make API call to get and return userid and last_activity"""
    last_activity = []
    response = requests.get(url=URL + '/Sessions', headers=headers, timeout=5)

    if response.status_code == 200:
        resp_data = response.json()
        if resp_data:
            for element in resp_data:
                last_activity.append((element['Id'], element['UserId'], element['LastActivityDate']))
            return last_activity
        else:
            print("Empty list received from the API.")
    else:
        print("Request failed with status code:", response.status_code)

def compare_time(users_list):
    """compare active time with current time"""
    current_time = datetime.now(timezone.utc)
    active_users = []
    for user_tuple in users_list:
        session_id, user_id, active_time = user_tuple
        active_time = parser.isoparse(active_time)
        time_difference = current_time - active_time
        if time_difference > timedelta(minutes=1):
            active_users.append((session_id, user_id))
    return active_users

def logout_idlers():
    """logout users who haven't done something for 30m"""
    last_activity_tuples = get_last_activity()
    idlers = compare_time(last_activity_tuples)

    for idler in idlers:
        session_id, user_id = idler
        response = requests.delete(url=URL + '/Sessions/' + session_id + '/User/' + user_id, headers=headers, timeout=5)
        test_concat = URL + '/Sessions/' + session_id + '/User/' + user_id
        print (session_id)
        print (user_id)
        print(test_concat)

        if response.status_code == 204:
            print("Session with ID", session_id, "has been deleted successfully.")
        else:
            print("Failed to delete session with ID:", session_id)
            print("Request failed with status code:", response.status_code)

logout_idlers()
