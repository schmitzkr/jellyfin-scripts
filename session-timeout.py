#Checks if a user is online, if they are, check the time of their last action, if it's over x seconds kick the user's session.
#https://api.jellyfin.org/#tag/User/operation/GetUsers

import requests
import json
import creds
from requests.auth import HTTPBasicAuth
headers = {'Content-Type': 'application/json',
        'accept': 'application/json',
        'Authorization': 'MediaBrowser Token="' + creds.token + '"'
        }

url = creds.host

response = requests.get(url = url+'/Users', headers=headers)
if response.status_code == 200:
    resp_data = response.json()
    if resp_data:
        for element in resp_data:
            print(element['LastActivityDate'])
            print(element['Name'])
            print(element['Id'])
    else:
        print("Empty list received from the API.")
else: 
    print("Request failed with status code:", response.status_code)



#print(resp_data[1])


