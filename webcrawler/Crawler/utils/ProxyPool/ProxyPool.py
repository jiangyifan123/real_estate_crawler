import requests
import socket

proxyPoolHost = "https://proxy.andyfanfan.myds.me/"
internal_host = "http://192.168.1.112:5010"
hostname = socket.gethostname()
LocalIP = socket.gethostbyname(hostname)
# 默认使用proxy跑
use_channel = False
internal = True


def get_https_proxy():
    host = internal_host if internal else proxyPoolHost
    return requests.get("{}/get?type=https".format(host)).json()


def get_http_proxy():
    host = internal_host if internal else proxyPoolHost
    return requests.get(f"{host}/get").json()


def delete_proxy(proxy):
    print('delete proxy: {}'.format(proxy))
    host = internal_host if internal else proxyPoolHost
    requests.get("{}/delete/?proxy={}".
                 format(host, proxy))


def requestByChannel(method, url, headers, data, cookies={}) -> requests.Response:
    # 隧道域名:端口号
    tunnel = "r951.kdltps.com:15818"

    # 用户名密码方式
    username = "t10151619356013"
    password = "0i247lpw"
    proxies = {
        "http": f"http://{username}:{password}@{tunnel}/",
        "https": f"http://{username}:{password}@{tunnel}/"
    }
    return requests.get(url, headers=headers, data=data, cookies=cookies, proxies=proxies)

def requestWithProxy(method, url, headers, data, cookies={}, useHttps=False) -> requests.Response:
    if use_channel:
        return requestByChannel(method, url, headers, data, cookies)
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
            html = requests.request(method, url, headers=headers, data=data, proxies=proxies, timeout=5, cookies=cookies)
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