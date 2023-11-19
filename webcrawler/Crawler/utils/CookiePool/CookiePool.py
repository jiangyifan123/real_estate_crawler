import requests
host = '127.0.0.1'
port = '5020'

def getCookie(website):
    response = requests.get(f'http://{host}:{port}/{website}/random')
    if response.status_code == 200:
        data = response.json()
        return ";".join([f"{k}={v}" for k, v in data.items()])
    return ""