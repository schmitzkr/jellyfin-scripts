"""end idle sessions on jellyfin instance"""
#!/usr/bin/env python

from datetime import datetime, timezone
from dateutil import parser
from datetime import timedelta
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

# def get_active_sessions():
#     """make api call to get and return sessionid, userid and last_activity"""
#     active_sessions = []
#     response = requests.get(url = URL+'/Sessions', headers=headers, timeout=5)
#     if response.status_code == 200:
#         resp_data = response.json()
#         if resp_data:
#             for element in resp_data:
#                 active_sessions.append((element['UserId'], element['LastActivityDate']))
#             return active_sessions
#         else:
#             print("Empty list received from the API.")
#     else:
#         print("Request failed with status code:", response.status_code)
# print(get_active_sessions())

# def compare_time(users_list):
#     """compare active time with current time"""
    
#     current_time = datetime.datetime.now().isoformat()+'Z'
#     active_users = []
#     print(current_time)
#     for user_tuple in users_list:
#         user_id, active_time = user_tuple
#         active_time = datetime.datetime.fromisoformat(active_time)
#         time_difference = current_time - active_time
#     if time_difference > timedelta(minutes=30):
#         active_users.append(user_id)
#     return active_users

def compare_time(users_list):
    """compare active time with current time"""
    
    current_time = datetime.datetime.utcnow()
    active_users = []
    print(current_time)
    

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
    
    print(active_users)
    return active_users

def logout_idlers():
    """compare the last active time with the current time, if it has been more than 30m, logout this user"""
    last_activity_tuples = get_last_activity()
    for tuple in last_activity_tuples:
        idlers = compare_time(last_activity_tuples)

logout_idlers()