import requests

try:
    response = requests.get("https://www.google.com", timeout=10)
    print("Success:", response.status_code)
except Exception as e:
    print(e)