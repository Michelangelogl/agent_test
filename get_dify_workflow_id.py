import requests

url = "https://api.dify.com/workflows"
headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
response = requests.post(url, json={"name": "Test Workflow"}, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Workflow ID:", data["data"]["workflow_id"])
else:
    print("Error:", response.status_code, response.text)