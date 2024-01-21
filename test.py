import requests

# Replace with the actual URL of your API
api_url = "http://127.0.0.1:7045/addUser"

# Sample data for the request
sample_data = {
    "userID": "kian",
    "username": "stinkypoop",
    "likesAvailable": 5,
}

# Sending a POST request to addResponse endpoint
response = requests.post(api_url, json=sample_data)

# Check the response from the server
if response.status_code == 200:
    print("Response added successfully")
else:
    print("Failed to add response. Status code:", response.status_code)
    print("Error:", response.text)
