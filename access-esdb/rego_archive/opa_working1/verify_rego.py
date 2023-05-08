import requests
import json

url = "http://localhost:8181/v1/data/auth/get_token"

payload = json.dumps({
    "input": {
        "user": "alice",
        "password": "alice1",
        "method": "GET",
        "path": ["read"]
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
