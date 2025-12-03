import requests
import json

headers = {
    'Authorization': 'Bearer app-A1S8q5NUQ2DwU3apgKwz5aPQ',
    'Content-Type': 'application/json'
}

payload = {
    'inputs': {},
    'response_mode': 'blocking',
    'user': 'test-user'
}

response = requests.post('https://api.dify.ai/v1/workflows/run', headers=headers, json=payload)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text}")
