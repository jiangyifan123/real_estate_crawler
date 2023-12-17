import requests
host = '192.168.1.158'
port = '5020'

def getCookie(website):
    response = requests.get(f'http://{host}:{port}/{website}/random')
    if response.status_code == 200:
        return response.json()
    return {}