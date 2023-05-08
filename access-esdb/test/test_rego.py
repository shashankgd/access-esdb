# Note these are not unit tests

import requests
import json


def test_get_token():
    url = "http://localhost:8181/v1/data/auth/get_token"

    payload = json.dumps({
        "input": {
            "user": "alice",
            "method": "DELETE",
            "path": ["movie-summary"]
        }
    })

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get('result') is not None:
            print("Token", data['result'])
        else:
            print("Invalid user and query combination")
    else:
        print("Error:", response.status_code)


######################

# Define function to verify username and password
def verify_username(username, password):
    url = "http://localhost:8181/v1/data/auth"

    payload = json.dumps({
        "input": {
            "username": username,
            "password": password
        }
    })

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url + "/verify_password", headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        print(data)
        if data.get('result') is not None:
            return data['result']
        else:
            return "Invalid username and password combination"
    else:
        return "Error: " + str(response.status_code)


def test_auth():
    print(verify_username("kelly", "kelly1"))
