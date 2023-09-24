import requests
from bs4 import BeautifulSoup
from ZillowModel import ZillowModel, SearchResponse
import json
import urllib
from ProxyPool import requestWithProxy
import traceback
import ZillowDao
from CustomLog import logged, logError


def getUrlByZipcode(zipcode: str, page: int) -> str:
    return "https://www.zillow.com/homes/%s_rb/%d_p/" % (zipcode, page)


def getUrlByCity(city: str) -> str:
    return "https://www.zillow.com/%s" % city

@logged()
def parseZillowHtml(content: str) -> tuple[list[ZillowModel], bool]:
    modelList = []
    soup = BeautifulSoup(content, 'lxml')
    scripts = soup.find_all("script", {"id": "__NEXT_DATA__"})
    if len(scripts) == 0:
        print("parse error")
        return [modelList, True]

    try:
        nextPageButton = soup.find("a", {"title": "Next page"})
        dataJsonString = scripts[0].text
        data = json.loads(dataJsonString)
        resultList = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]
        for result in resultList:
            model = ZillowModel.from_json(json.dumps(result))
            modelList.append(model)
        return [modelList, nextPageButton.get("aria-disabled") == "true"]
    except Exception as e:
        print(e)
        logError(traceback.format_exc())

    return [modelList, True]

@logged()
def getDataByZipcode(zipcode, page=1) -> tuple[list[ZillowModel], bool]:
    url = getUrlByZipcode(zipcode, page)

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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'mode': 'no-cors',
    }

    response = requestWithProxy("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print('{} status code {}'.format(url, response.status_code))
        return [[], True]

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
def getResultByCity(city: str, page: int = 1) -> list[ZillowModel] | None:
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
        return None
    
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
    return allModelList

@logged()
def getEstateByFuzzySearch(searchText) -> list[ZillowModel] | None:
    suggestions = getSuggestions(searchText)
    if suggestions is None or len(suggestions.results) == 0:
        return

    regionType = suggestions.results[0].metaData.regionType
    display = suggestions.results[0].display
    if regionType in ["city", "neighborhood"]:    
        cityName = ''.join(display.strip('').replace(' ', '-').lower().split(','))
        return getAllResultByCity(cityName)
    elif regionType == "zipcode":
        return getAllDataByZipcode(display)
    elif regionType == "Address":
        pass
    return None


if __name__ == "__main__":
    pass
    # getDataByZipcode(98121)
    # modelList = getEstateByFuzzySearch("las vegas")
    # modelList = getEstateByFuzzySearch("98121")
    modelList = getEstateByFuzzySearch("seattle")
    ZillowDao.insertModelList(modelList)