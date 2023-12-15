import json
from cookiespool.config import *
from cookiespool.db import *
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

__all__ = ['app']

class Conn:
    def __init__(self):
        super(Conn, self).__init__()
        self.update_conn()        

    def update_conn(self):
        """
        获取
        :return:
        """
        for website in GENERATOR_MAP:
            print(website)
            if not hasattr(self, website):
                setattr(self, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
                setattr(self, website + '_accounts', eval('RedisClient' + '("accounts", "' + website + '")'))
        return self

    def get_conn(self):
        return self.update_conn()


app = FastAPI()
conn = Conn()

def start_api():
    import uvicorn
    print("Running the FastAPI application")
    uvicorn.run("cookiespool.api.main:app", host=API_HOST, port=API_PORT, reload=True)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get('/{website}/random')
def random(website: str):
    """
    获取随机的Cookie, 访问地址如 /weibo/random
    :return: 随机Cookie
    """
    g = conn.get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return json.loads(cookies)


@app.get('/{website}/add/{username}/{password}')
def add(website: str, username: str, password: str):
    """
    添加用户, 访问地址如 /weibo/add/user/password
    :param website: 站点
    :param username: 用户名
    :param password: 密码
    :return: 
    """
    g = conn.get_conn()
    print(username, password)
    getattr(g, website + '_accounts').set(username, password)
    return json.dumps({'status': '1'})


@app.get('/<website>/count')
def count(website):
    """
    获取Cookies总数
    """
    g = conn.get_conn()
    count = getattr(g, website + '_cookies').count()
    return json.dumps({'status': '1', 'count': count})