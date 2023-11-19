import requests
import socket
import logging

proxyPoolHost = "https://proxy.andyfanfan.myds.me"
internal_host = "http://192.168.1.112:5010"
hostname = socket.gethostname()
LocalIP = socket.gethostbyname(hostname)
#默认使用proxy跑
use_proxy = True
internal = True

def get_https_proxy():
    host = internal_host if internal else proxyPoolHost
    return requests.get("{}/get?type=https".format(host)).json()

def get_http_proxy():
    host = internal_host if internal else proxyPoolHost
    return requests.get("{}/get".format(host)).json()

def delete_proxy(proxy):
    print('delete proxy: {}'.format(proxy))
    host = internal_host if internal else proxyPoolHost
    requests.get("{}/delete/?proxy={}".
                 format(host, proxy))

def requestWithProxy(method, url, headers, data, useHttps=False) -> requests.Response:
    if not use_proxy:
        return requests.request(method, url, headers=headers, data=data)
    # ....
    retry_count = 5
    if useHttps:
        proxy = get_https_proxy().get("proxy")
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    else:
        proxy = get_http_proxy().get("proxy")
        proxies = {"http": f"http://{proxy}"}
    while retry_count > 0:
        try:
            html = requests.request(method, url, headers=headers, data=data, proxies=proxies, timeout=5)
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    response = requests.Response()
    response.status_code == 500
    print(f'get {url} fail')
    return response