import ApiUtils
import ZillowDao
import ProxyPool

CityList = [
    "Dallas",
    "Houston",
    "Austin",
    "Pittsburgh",
    "Nashville",
    "Lafayette",
    "Las Vegas",
    "Chandler",
    "Charlotte",
    "Atlanta",
]

ZipcodeList = {
    "Dallas": (75201,75398),
    "Houston": (77001, 77299),
}

def crawlerTask():
    def InsertData(searchText):
        modelList = ApiUtils.getEstateByFuzzySearch(searchText)
        ZillowDao.upsertModelList(modelList)
    
    def checkCityExist(city):
        suggestions = ApiUtils.getSuggestions(city)
        return "{} exist:{}".format(city, suggestions is not None and len(suggestions.results) != 0)
    
    for city in CityList:
        InsertData(city)

def crawlerTask2():
    def InsertData(searchText):
        modelList = ApiUtils.getEstateByFuzzySearch(searchText)
        ZillowDao.upsertModelList(modelList)
    
    def checkCityExist(city):
        suggestions = ApiUtils.getSuggestions(city)
        return "{} exist:{}".format(city, suggestions is not None and len(suggestions.results) != 0)
    
    for city, zipCodeRange in ZipcodeList.items():
        for zipcode in range(zipCodeRange[0], zipCodeRange[1] + 1):
            InsertData(zipcode)

if __name__ == "__main__":
    if ProxyPool.internal:
        with open("/path/to/appdata/config/project/real-est/real_estate_crawler/webcrawler/ZillowCrawler/logs/tasks.log", "a+") as f:
            f.write("crawlerTasks start\n")
    crawlerTask()
    # crawlerTask2()