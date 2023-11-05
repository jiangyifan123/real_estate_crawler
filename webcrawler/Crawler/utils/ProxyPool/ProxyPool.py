import requests
import socket
import time
import random

proxyPoolHost = "https://proxy.andyfanfan.myds.me"
internal_host = "http://192.168.1.112:5010"
hostname = socket.gethostname()
LocalIP = socket.gethostbyname(hostname)
#默认使用proxy跑
use_proxy = True
internal = True
proxypool_url = 'http://192.168.1.112:5555/random'
Random = random.Random()

def get_proxy():
    host = internal_host if internal else proxyPoolHost
    return requests.get("{}/get/".format(host)).json()


def delete_proxy(proxy):
    print('delete proxy: {}'.format(proxy))
    host = internal_host if internal else proxyPoolHost
    requests.get("{}/delete/?proxy={}".
                 format(host, proxy))

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    proxy = requests.get(proxypool_url).text.strip()
    proxies = {'http': 'http://' + proxy}
    return proxies

def requestWithProxy(method, url, headers, data) -> requests.Response:
    # stopCount = Random.randint(1, 2)
    # time.sleep(stopCount)
    # if (stopCount % 2 == 0):
    #     return requestWithProxy2(method, url, headers, data)
    # else:
    #     return requestWithProxy1(method, url, headers, data)
    return requestWithProxy1(method, url, headers, data)

def requestWithProxy1(method, url, headers, data) -> requests.Response:
    if not use_proxy:
        return requests.request(method, url, headers=headers, data=data)
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.request(method, url, headers=headers, data=data,
                                    proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    response = requests.Response()
    response.status_code == 500
    return response

def requestWithProxy2(method, url, headers, data) -> requests.Response:
    proxies = get_random_proxy()
    try:
        html = requests.request(method, url, headers=headers, data=data,
                                    proxies=proxies)
        return html
    except Exception:
        response = requests.Response()
        response.status_code == 500
        return response