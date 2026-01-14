import requests
resp = requests.get('http://127.0.0.1:8000/')
print(resp.text)
print(resp.status_code)