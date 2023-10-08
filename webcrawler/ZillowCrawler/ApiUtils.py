import requests
from bs4 import BeautifulSoup
from Models import ZillowModel, SearchResponse, ZillowDetailPage
import json
import urllib
from ProxyPool import requestWithProxy
import traceback
import ZillowDao
from CustomLog import logged, logError, logDebug

def getUrlByZipcode(zipcode: str, page: int) -> str:
    return "https://www.zillow.com/homes/%s_rb/%s/" % (zipcode, "%d_p" % page if page > 1 else "")


def getUrlByCity(city: str) -> str:
    return "https://www.zillow.com/%s" % city

@logged()
def parseZillowHtml(content: str) -> tuple[list[ZillowModel], bool]:
    modelList = []
    soup = BeautifulSoup(content, 'lxml')
    scripts = soup.find_all("script", {"id": "__NEXT_DATA__"})
    if len(scripts) == 0:
        print("parse error")
        return (modelList, True)

    try:
        nextPageButton = soup.find("a", {"title": "Next page"})
        dataJsonString = scripts[0].text
        data = json.loads(dataJsonString)
        resultList = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]
        for result in resultList:
            model = ZillowModel.from_json(json.dumps(result))
            modelList.append(model)
        return (modelList, nextPageButton is None or nextPageButton.get("aria-disabled", "true") == "true")
        # return (modelList, True)
    except Exception as e:
        print(e)
        logError(traceback.format_exc())

    return (modelList, True)

@logged()
def parseZillowDetailHtml(content: str) -> ZillowDetailPage:
    model = None
    soup = BeautifulSoup(content, 'lxml')
    scripts = soup.find_all("script", {"id": "__NEXT_DATA__"})
    if len(scripts) == 0:
        print("parse error")
        return model

    try:
        dataJsonString = scripts[0].text
        data = json.loads(dataJsonString)
        detailData = json.loads(data["props"]["pageProps"]["gdpClientCache"])
        values = detailData.values()
        if len(values) < 1:
            return model
        property = list(values)[0]["property"]
        model = ZillowDetailPage.from_json(json.dumps(property))
        model.num_garage = property.get("resoFacts", {}).get("garageParkingCapacity",None)
        model.status_text = property.get("attributionInfo", {}).get("trueStatus", None)
        return model
    except Exception as e:
        print(e)
        logError(traceback.format_exc())
    finally:
        return model

@logged()
def getDataByZipcode(zipcode, page=1) -> tuple[list[ZillowModel], bool]:
    url = getUrlByZipcode(zipcode, page)
    payload = {}
    headers = {
    'authority': 'www.zillow.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'JSESSIONID=F2DE6DF8FC67940EBD95997543678B82; zguid=24|%244f68cb06-c00b-494d-975d-5d99781a90de; zgsession=1|8b2e4b1b-6c00-4e6e-9de4-4143486ea057; tfpsi=2a530b2c-b27a-4289-9c34-358be179bb28; _ga=GA1.2.1286085892.1696727940; _gid=GA1.2.1552879356.1696727940; zjs_anonymous_id=%224f68cb06-c00b-494d-975d-5d99781a90de%22; zjs_user_id=null; zg_anonymous_id=%22192b12c1-bccc-45b9-90ba-d348a69cfc38%22; pxcts=a93a4cd9-6578-11ee-8389-c809c036803d; _pxvid=a93a3a66-6578-11ee-8389-8060146a0939; _gcl_au=1.1.314056997.1696727941; DoubleClickSession=true; __pdst=4029497d387e46abb83a30f2fa4bee12; _clck=5e57ta|2|ffo|0|1376; _pin_unauth=dWlkPVl6a3dOVEpqTkRRdE9XRTJaQzAwWWpnM0xXSXhaVFF0T1RCa09EVTFOREpoTWpCaQ; AWSALB=vn10qfYPyQ83spAiH1H0TvIHxn/rmG1XsSPWfGd+l1UNDlb74A6f1lRQ3rUx7W8LcYjeHE/cYCUMRX8i6DyiXhf2ANey3V6AV+f2qcRBraklow/l0fVd6lLGtzgZ; AWSALBCORS=vn10qfYPyQ83spAiH1H0TvIHxn/rmG1XsSPWfGd+l1UNDlb74A6f1lRQ3rUx7W8LcYjeHE/cYCUMRX8i6DyiXhf2ANey3V6AV+f2qcRBraklow/l0fVd6lLGtzgZ; search=6|1699320337481%7Crect%3D32.79900746614807%2C-96.78929111364747%2C32.75679132932848%2C-96.81830188635254%26rid%3D90755%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0990755%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _px3=21a828eaa1d86133ec223180698e0c8b470064509a291b97f6fa42b2d7d21ceb:kvm+7Z1fuBdXZr75goo9xdfZDzPjRlMJbPZQlI9sYE9A956ElyJGmTl2DO4pJYxiz07RmwEeBwRbO+8LjDf9VQ==:1000:EmKM8Me998jgQIenK3nq143+1yubSfTr9qlnBWL4vGtx5bhCpLk1MH3XQbjq1L/OGJ4UFWNYtKKRgskr0Pqi3XRsDGP8cZ8WQEYt7oszZZAdnGpN5Oy64uOGx/SH8OLkV6fnyTk7Z7MAkUK8CM66YZm4/leRdV/PslV+11NxD1RSNdGSOkKIF3G/NMjQv7dX0su6vd29TfeVXzRjbOOhvqXoPWtQyxv6UMRHC33YID8=; __gads=ID=5e2ce1b56345422c:T=1696727941:RT=1696728338:S=ALNI_MZj9175YVRHW-WJ9bIzxwjQH__9uA; __gpi=UID=00000d97a24abed1:T=1696727941:RT=1696728338:S=ALNI_MZOSmMg8ckKzav8n5WIuDRqspc6vQ; _uetsid=288700d0657711eea33edf2cf01cbdbb; _uetvid=03ffc3e04f9311ee8b15e72c41dbe29d; _clsk=7qmzrb|1696728338479|4|0|s.clarity.ms/collect; search=6|1699320481317%7Crb%3D75201%26rect%3D32.802623%252C-96.783247%252C32.77261%252C-96.81563%26sort%3Dpriorityscore%09%0990754%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; zgsession=1|a28ff679-6c63-4874-9851-2aa7ae14329c; zguid=24|%24c2919238-9456-41f3-8ca4-19c1b30ae423; AWSALB=+JUSuZGTHLF5UqGDzHuyuo/ZBNCGsTyoieIturi+mRNCLRRsSTGwVXX6+z9iOWjA08fEFtXHADYOHKG4i1rtQTmheDsmvQPGTbP2BhXuJVMUVc/5qpGlyPn06Rly; AWSALBCORS=+JUSuZGTHLF5UqGDzHuyuo/ZBNCGsTyoieIturi+mRNCLRRsSTGwVXX6+z9iOWjA08fEFtXHADYOHKG4i1rtQTmheDsmvQPGTbP2BhXuJVMUVc/5qpGlyPn06Rly; JSESSIONID=89D94D12A474A9AF2DEA9AFA941B4212',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = requestWithProxy("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print('{} status code {}'.format(url, response.status_code))
        return ([], True)
    
    Collect(url)

    return parseZillowHtml(response.content)

@logged()
def getAllDataByZipcode(zipcode) -> list[ZillowModel]:
    pMax = 20
    allModelList = []
    for page in range(1, pMax):
        modelList, isLastPage = getDataByZipcode(zipcode, page)
        allModelList.extend(modelList)
        if isLastPage:
            break
    logDebug("get data by {} result len: {}".format(zipcode, len(allModelList)))
    return allModelList


def getSearchResult():
    link = 'https://www.zillow.com/search/GetSearchPageState.htm?'

    params = {
        'searchQueryState': {
            "pagination": {},
            "usersSearchTerm": "Seattle",
            "regionSelection": [{"regionId": 250206}],
            "isMapVisible": False,
            # "mapBounds": {"north": 47.734145,
            #               "east": -122.224433,
            #               "south": 47.491912,
            #               "west": -122.465159
            #             },
            "filterState": {
                "doz": {"value": "6m"}, "isForSaleByAgent": {"value": False},
                "isForSaleByOwner": {"value": False}, "isNewConstruction": {"value": False},
                "isForSaleForeclosure": {"value": False}, "isComingSoon": {"value": False},
                "isAuction": {"value": False}, "isPreMarketForeclosure": {"value": False},
                "isPreMarketPreForeclosure": {"value": False},
                "isRecentlySold": {"value": True}, "isAllHomes": {"value": True},
                "hasPool": {"value": True}, "hasAirConditioning": {"value": True},
                "isApartmentOrCondo": {"value": False}
            },
            "isListVisible": True,
            "mapZoom": 11
        },
        'wants': {"cat1": ["listResults"]},
        'requestId': 2
    }

    with requests.Session() as s:
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        s.headers["x-requested-session"] = "BE6D8DA620E60010D84B55EB18DC9DC8"
        s.headers["cookie"] = f"JSESSIONID={s.headers['x-requested-session']}"
        data = json.dumps(
            json.loads(s.get(f"{link}{urllib.parse.urlencode(params)}").content),
            indent=2
        )
        with open("citySearchSample.json", "w") as f:
            f.write(data)

@logged()
def getSuggestions(searchText: str) -> SearchResponse | None:
    params = {
        "q": searchText,
        "resultTypes": "allRegion,allAddress",
        "abKey": "acb00326-9a70-42e6-a1f7-eda19d1bcd71",
        "clientId": "static-search-page"
    }

    url = "https://www.zillowstatic.com/autocomplete/v3/suggestions?%s" %(urllib.parse.urlencode(params))

    payload = {}
    headers = {
        'authority': 'www.zillowstatic.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://www.zillow.com',
        'referer': 'https://www.zillow.com/homes/for_sale/?searchQueryState=%7B%22usersSearchTerm%22%3A%2298121%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.369576%2C%22east%22%3A-122.33402%2C%22south%22%3A47.609886%2C%22north%22%3A47.618615%7D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requestWithProxy("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print('{} status code {}'.format(url, response.status_code))
        return None

    try:
        result = SearchResponse.from_json(response.content)
        return result
    except Exception as e:
        print(e)
        logError(traceback.format_exc())

    return None

@logged()
def getResultByCity(city: str, page: int = 1) -> tuple[list[ZillowModel], bool] | None:
    url = "https://www.zillow.com/%s/%d_p" % (city, page)
    payload = {}
    headers = {
        'authority': 'www.zillow.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requestWithProxy("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print('{} status code {}'.format(url, response.status_code))
        return ([], True)
    
    Collect(url)
    return parseZillowHtml(response.content)

@logged()
def getAllResultByCity(city) -> list[ZillowModel] | None:
    pMax = 30
    allModelList = []
    for page in range(1, pMax):
        modelList, isLastPage = getResultByCity(city, page)
        allModelList.extend(modelList)
        if isLastPage:
            break
    logDebug("get {} result len: {}".format(city, len(allModelList)))
    return allModelList

# zillo fuzzy search
@logged()
def getEstateByFuzzySearch(searchText) -> list[ZillowModel] | None:
    suggestions = getSuggestions(searchText)
    if suggestions is None or len(suggestions.results) == 0:
        return []

    regionType = suggestions.results[0].metaData.regionType
    display = suggestions.results[0].display
    modelList = []
    if regionType in ["city", "neighborhood"]:    
        cityName = ''.join(display.strip('').replace(' ', '-').lower().split(','))
        modelList = getAllResultByCity(cityName)
        # return [getZillowDetailPage(model.detailUrl) for model in modelList]
    elif regionType == "zipcode":
        modelList = getAllDataByZipcode(display)
        # return [getZillowDetailPage(model.detailUrl) for model in modelList]
    elif regionType == "Address":
        pass
    return modelList

@logged()
def getZillowDetailPage(detailUrl):
    payload = {}
    headers = {
    'authority': 'www.zillow.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': r'zguid=24|%24acb00326-9a70-42e6-a1f7-eda19d1bcd71; zjs_anonymous_id=%22acb00326-9a70-42e6-a1f7-eda19d1bcd71%22; zjs_user_id=null; zg_anonymous_id=%226c75c121-7d14-4ffc-b7e3-0ce834e02a75%22; _ga=GA1.2.1950585950.1694320334; _pxvid=00cacf70-4f93-11ee-905a-9b35bb49d730; _gcl_au=1.1.981758905.1694320334; __pdst=fb867bfacb1e4ad58a69920429f29855; _fbp=fb.1.1694320334148.856932049; _pin_unauth=dWlkPU9XTXhaVE5qTXpRdE1UYzRNeTAwWXpCa0xXRXlOalF0TVRjNE5tVmtZak5oWkRSbA; FSsampler=962613034; _hp2_id.1215457233=%7B%22userId%22%3A%225541294366932229%22%2C%22pageviewId%22%3A%225124666665405135%22%2C%22sessionId%22%3A%228504840435051524%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; g_state={"i_p":1698556971033,"i_l":4}; _gid=GA1.2.2039922503.1696307236; zgsession=1|1f114d0b-bd78-4cc0-8703-588df2ae51f4; pxcts=ae9f71d9-61cd-11ee-a3a1-956716f9b366; DoubleClickSession=true; _clck=gw9qia|2|ffm|0|1348; JSESSIONID=806D2613E4EF7B428BD111E4CDB3073B; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_cfp=1; _pxff_bsco=1; _gat=1; _px3=9618a262896f38f67a0502720a6537efed8d69224a92e32f6d17e7e78f4e143f:GUWrULwBAeOz9Msh5MlWiHOpm+nsi+eZLqOd3BR0ZiZ9s/qBFHbVbGBusc5dp8KPwBF3Dq5Nwok+fZYE/dgYxA==:1000:4Wt/F9XuWERQ9cX2ZZRZZe9dqNitu28aWpSJtJW/Sw9PCYQDmLbhzwHTgFnWMNgSWTdbUsAP5Lv1Jq+OPB278NNoFh/y4OhvOa3SmqAxZyWI38VrUBzYTawND4x4UAMZINQ0ATN9hmE5e4QKYsJ5cF31zu+mlsqoG3KWwDZkAHydJzMQ36qAu2E+eURA0qqkNjrLBw51mDftknCuvASMipDOEZlQmrD0hziIhJcWxsc=; search=6|1699164108332%7Crect%3D37.365655037338904%252C-121.85400009155273%252C37.28579942182216%252C-122.08488464355469%26rid%3D13713%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0999580%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; AWSALB=tTT7GIGe9XgOgCCcZggoCOGBaFZ4+tYakF5evMHX1xnIxiukY+dfhMNjQx3t8Bht1ch/HJHMLJy0svQmFOBB9McKGfHUm2RlrGr669o3CcZaGj1mQpBZ8DHVBUUW; AWSALBCORS=tTT7GIGe9XgOgCCcZggoCOGBaFZ4+tYakF5evMHX1xnIxiukY+dfhMNjQx3t8Bht1ch/HJHMLJy0svQmFOBB9McKGfHUm2RlrGr669o3CcZaGj1mQpBZ8DHVBUUW; _uetsid=2389628061a511eeb08c2f4d30bb3c4a; _uetvid=03ffc3e04f9311ee8b15e72c41dbe29d; tfpsi=f1ab2125-e9fb-44cb-bbb4-b8f1a2e22e78; _clsk=atle44|1696572108907|1|0|z.clarity.ms/collect; __gads=ID=3e3a9a68d3a8472d:T=1694918441:RT=1696572110:S=ALNI_MZxnAIVNGbs-1Zp6pfVqakuyf-zCw; __gpi=UID=00000d9371d4dbb3:T=1694918441:RT=1696572110:S=ALNI_MZeryHVZvpEiSvolcNE5R2eX71SiA; search=6|1699003862391%7Czpid%3D49146814%26sort%3Dpriorityscore%09%0918959%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; zgsession=1|a28ff679-6c63-4874-9851-2aa7ae14329c; zguid=24|%24c2919238-9456-41f3-8ca4-19c1b30ae423; AWSALB=7evVhMGiGzyhDpqbxugMFFKQGEr9jws+5KAOiVInkR1bdRWZDpSCEKGkBaT4hM+HBPIBytwMVl5wCmbMkvZrhvXg2r0NYp0mblmJ2rOklYY3kfk+yvLL1K2QYSo3; AWSALBCORS=7evVhMGiGzyhDpqbxugMFFKQGEr9jws+5KAOiVInkR1bdRWZDpSCEKGkBaT4hM+HBPIBytwMVl5wCmbMkvZrhvXg2r0NYp0mblmJ2rOklYY3kfk+yvLL1K2QYSo3; JSESSIONID=4B3F4B648D1CCA9E8F5247176F4DE21A',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = requestWithProxy("GET", detailUrl, headers=headers, data=payload)
    if response.status_code != 200:
        print('{} status code {}'.format(detailUrl, response.status_code))
        return None

    return parseZillowDetailHtml(response.content)

def Collect(referer):
    url = "https://s.clarity.ms/collect"

    payload = '%5E%1F%5E%C2%8B%5E%08%5E='
    headers = {
    'Accept': 'application/x-clarity-gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'MUID=00CDE08798B668970DFCF3239932696B',
    'Origin': 'https://www.zillow.com',
    'Referer': referer,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

if __name__ == "__main__":
    url = "https://www.zillow.com/homedetails/79-E-Agate-Ave-UNIT-401-Las-Vegas-NV-89123/55110557_zpid/"
    print(getZillowDetailPage(url))
    # test = getEstateByFuzzySearch("seattle")
    # print(test[0])