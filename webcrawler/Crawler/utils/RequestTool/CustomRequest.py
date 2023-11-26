from utils.ProxyPool.ProxyPool import requestWithProxy
from utils.UserAgent.UserAgentTools import random_user_agent
from utils.CookiePool.CookiePool import getCookie
import requests

def request(method, url, headers={}, data={}, cookieKey="", tryCount=10, useHttps=False):
    if tryCount <= 0:
        return None
    headers['user-agent'] = random_user_agent()
    cookies = {}
    if cookieKey != "":
        cookies = getCookie(cookieKey)
    response = requestWithProxy(method, url, headers, data, cookies, useHttps)
    if response.status_code != 200:
        print(f'{url} status code {response.status_code} tryCount: {tryCount}')
        return request(method, url, headers, data, cookieKey, tryCount-1, useHttps)
    return response