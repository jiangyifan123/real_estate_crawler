import requests

from cookiespool.db import RedisClient
from cookiespool.account_info import accountInfo

def scan():
    print("importing account info")
    for website, account_info in accountInfo.items():
        conn = RedisClient('accounts', website)
        for username, password in account_info.items():
            result = conn.set(username, password)
            if not result:
                print(f'import {username} faile')
    print("import account info complete")

if __name__ == '__main__':
    scan()