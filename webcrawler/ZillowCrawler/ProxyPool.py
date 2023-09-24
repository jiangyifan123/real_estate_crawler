import requests

proxyPoolIP = "192.168.1.112"
port = 5010
#默认使用proxy跑
use_proxy = True


def get_proxy():
    return requests.get("http://{}:{}/get/".format(proxyPoolIP, port)).json()


def delete_proxy(proxy):
    requests.get("http://{}:{}/delete/?proxy={}".
                 format(proxyPoolIP, port, proxy))


def requestWithProxy(method, url, headers, data) -> requests.Response:
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
