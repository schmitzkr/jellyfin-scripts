"""end idle sessions on jellyfin instance"""
#!/usr/bin/env python

from datetime import datetime, timezone
from datetime import timedelta
from dateutil import parser
import requests
import creds

headers = {'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': 'MediaBrowser Token="' + creds.TOKEN + '"'
        }

URL = creds.HOST

def get_last_activity():
    """make api call to get and return userid and last_activity"""
    last_activity = []
    response = requests.get(url = URL+'/Users', headers=headers, timeout=5)
    if response.status_code == 200:
        resp_data = response.json()
        if resp_data:
            for element in resp_data:
                last_activity.append((element['Id'], element['LastActivityDate']))
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
        user_id, active_time = user_tuple
        active_time = parser.isoparse(active_time)
        time_difference = current_time - active_time
        if time_difference > timedelta(minutes=30):
            active_users.append(user_id)
    return active_users

def logout_idlers():
    """logout users who haven't done something for 30m"""
    last_activity_tuples = get_last_activity()
    for tuple_pair in last_activity_tuples:
        idlers = compare_time(last_activity_tuples)
    print(idlers)
    #need to add something here to actually logout idlers, there doesnt seem to be an api endpoint.
logout_idlers()
