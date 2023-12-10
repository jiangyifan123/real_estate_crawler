from utils.ProxyPool.ProxyPool import requestWithProxy
from utils.UserAgent.UserAgentTools import random_user_agent
from utils.CookiePool.CookiePool import getCookie
import requests
from http.cookies import SimpleCookie

def request(method, url, headers={}, data={}, cookieKey="", tryCount=3, useHttps=False, useProxy=False):
    if tryCount <= 0:
        return None
    headers['user-agent'] = random_user_agent()
    cookies = {}
    if cookieKey != "":
        if cookieKey == 'zillow':
            rawcookies = r"x-amz-continuous-deployment-state=AYABeBgVNPaZrq74EVpCTpLbd80APgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADJHLYsoyxTOZkRY6MgAwiQi0v1B%2FvFq0+MXP4NuLXpQvvXAEC1NQR+uIeeYL%2FZHj2LaqPk%2F0p7DSBwJM0W5aAgAAAAAMAAQAAAAAAAAAAAAAAAAAAH7X3xxcoN%2FkinfaAfSVmmn%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAyOxjKuA8jqyy8GTOOHHuirXeLpUN78gMT144T%2F; zguid=24|%2465550fb3-402c-402f-b400-7928606d37bb; zgsession=1|448416b7-99cd-4883-b648-582709f1234a; zjs_anonymous_id=%2265550fb3-402c-402f-b400-7928606d37bb%22; zg_anonymous_id=%22b4597df6-67d8-4358-8762-2a44da80aa56%22; _ga=GA1.2.218245435.1702165050; _gid=GA1.2.317467819.1702165050; pxcts=eb50d098-96eb-11ee-9852-a44cc73b4a58; _pxvid=eb50c5dd-96eb-11ee-9852-6cb5097b00dd; _gcl_au=1.1.134146148.1702165051; DoubleClickSession=true; __pdst=c2ded62a22344788a84c3cf1ea092f61; _fbp=fb.1.1702165051305.803930853; tfpsi=0478f1f1-fd95-4626-bbd2-b5db4fa394c4; _pin_unauth=dWlkPU1XUmtNREE1WmpVdFlqTXpPQzAwTkdNeUxXRmtNVEl0TURKaE56Y3paV1kxT0dKbA; _hp2_ses_props.1215457233=%7B%22ts%22%3A1702165050984%2C%22d%22%3A%22www.zillow.com%22%2C%22h%22%3A%22%2F%22%7D; _clck=1lqrp8s%7C2%7Cfhe%7C0%7C1438; JSESSIONID=7B38C510F00BF0C73D75C7B9DFD1D690; ZILLOW_SSID=1|AAAAAVVbFRIBVVsVEj%2Be9bSpXiucMaI7jn6AHPeMpJJvjzH3ht9uDmG7zdrWtGISwiwo60D5HZ1bU2Anhp20xvnvUBXe2OGp1w; loginmemento=1|d86c1a03a0b21c26adc6295fd677506b27d69f5a56a045e2391938a954aedb58; userid=X|3|b949881b32567a3%7C10%7CTwwsYB-8IVsjgeoSQ10CQ0cjzlzbwpns3vFbLsjXj0Y%3D; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEuNMMbyV3oEpFth%2FaOpvsgaSuKKS9m68pBQlQEecsI2moi7EpJI1wpj5dpBPjX5uqIjIjM9AVymhBps9XQ; zjs_user_id=%22X1-ZU16vsvb6b016vd_8nu8j%22; x-amz-continuous-deployment-state=AYABeIMCMX1CcbBX5F0DKumz9TIAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADOfQ%2Fn2shjdl4R08mAAwdxBCzSvEruoCMZ3oB7tz45m5Zh74KuVQRddtnhtI+0KaEU3dAHhCvDMBt7EVnedsAgAAAAAMAAQAAAAAAAAAAAAAAAAAAFlC9RRQgv3FZq3N1JW87Bn%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAxuHluVEh%2FTPrIW0OuqskBIJwX7qA5MCd46edFZX7qA5MCd46edFQ==; _hp2_id.1215457233=%7B%22userId%22%3A%224650714568455652%22%2C%22pageviewId%22%3A%226697866127476415%22%2C%22sessionId%22%3A%22315911413968424%22%2C%22identity%22%3A%22X1-ZU16vsvb6b016vd_8nu8j%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D; _gat=1; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_cfp=1; _pxff_bsco=1; _px3=b8e4cc44ddf25caa169787944fd23f438e4ce5af47d30c7632b92fad4595530b:WuCbL2i/kYGtpQTWVnfdD7SM5gyDF6t80Y4+lHdoqFKpCZVyTkXE7+EG2zVhaIR0ZPD7h7R674yvrSIe1LwQGQ==:1000:tM5VLoWUP5r/zgqAsyOBgPqrkQZmY7N2hZvtuKrfXHDZbf+86PFFxf+9wEPHwBSl1UW6JW6KbZUxJdXcA0qcOD5H/QrQW2MOudjZkVDGWh76LTodpMLzMqZ270fW4eMpxtm66dOmJ+wAYiyy7khKhtegU/9OojUR3FYspp4ps969rKLZvb6M5bexEtpwYvCAvtypnOz6qZYOL4qUCQM5adcAX+NvZRmJDe5HWhWnT6I=; search=6|1704757423772%7Crect%3D39.09078759670635%2C-120.37928955078125%2C36.39823246967924%2C-124.46071044921875%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%09%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _uetsid=eb9ff98096eb11ee9c06078cdb2fef90; _uetvid=eba0228096eb11ee97afb9b9f89ad904; _clsk=wrcfyx%7C1702165424813%7C3%7C0%7Cw.clarity.ms%2Fcollect; __gads=ID=93953efa6922d496:T=1702165424:RT=1702165424:S=ALNI_MakuSfa5cOFZ3GXMGmxUEDLMwLX6w; __gpi=UID=00000da7f6295a54:T=1702165424:RT=1702165424:S=ALNI_Mas45tASumFG4OUcPPSCUkwEXPoOw; AWSALB=I4/8x5H5sTiA/VU7f4vYExMdCovTruoJGsvsLD1/6m10OxYUW7ivFv+/9dyxviQZ+uBZGaFxqllTnlvRsJvenSEnSiR7je7YAerlHO6cwrAAfkztYREiOIlQhOkk; AWSALBCORS=I4/8x5H5sTiA/VU7f4vYExMdCovTruoJGsvsLD1/6m10OxYUW7ivFv+/9dyxviQZ+uBZGaFxqllTnlvRsJvenSEnSiR7je7YAerlHO6cwrAAfkztYREiOIlQhOkk"
            cookieTool = SimpleCookie()
            cookieTool.load(rawcookies)
            cookies = {k: v.value for k, v in cookieTool.items()}
        else:
            cookies = getCookie(cookieKey)
    try:
        if useProxy:
            response = requestWithProxy(method, url, headers, data, cookies, useHttps)
        else:
            response = requests.request(method, url, headers=headers, data=data, cookies=cookies)
    except Exception as e:
        pass
    if response.status_code != 200:
        print(f'{url} status code {response.status_code} tryCount: {tryCount}')
        return request(method, url, headers, data, cookieKey, tryCount-1, useHttps, useProxy)
    return response