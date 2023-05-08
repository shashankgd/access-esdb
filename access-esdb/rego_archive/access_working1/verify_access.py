import requests
import json

url = "http://localhost:8080/cars/test-car"
headers = {
    "Authorization": "alice",
    "Content-Type": "application/json"
}
data = {
    "model": "Toyota",
    "vehicle_id": "357192",
    "owner_id": "..."
}

response = requests.put(url, headers=headers, data=json.dumps(data))

assert response.status_code == 200


headers = {
    "Authorization": "kelly",
    "Content-Type": "application/json"
}
data = {
}

response = requests.delete(url, headers=headers, data=json.dumps(data))
assert response.status_code == 403

