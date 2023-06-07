"""end idle sessions on jellyfin instance"""
#!/usr/bin/env python

import datetime
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
print(get_last_activity())

def get_active_sessions():
    """make api call to get and return sessionid, userid and last_activity"""
    active_sessions = []
    response = requests.get(url = URL+'/Sessions', headers=headers, timeout=5)
    if response.status_code == 200:
        resp_data = response.json()
        if resp_data:
            for element in resp_data:
                active_sessions.append((element['UserId'], element['LastActivityDate']))
            return active_sessions
        else:
            print("Empty list received from the API.")
    else:
        print("Request failed with status code:", response.status_code)
print(get_active_sessions())
