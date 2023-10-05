from BaseDecorator import fetchSql, execSqls
from CustomLog import logged
from Models import ZillowModel, Properties, ZillowDetailPage

@fetchSql
@logged()
def getTables():
    return """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""

@fetchSql
@logged()
def getRawProperties():
    return """SELECT * FROM "raw.properties";"""

@execSqls
@logged()
def insertModelList(modelList: list[ZillowModel]):
    def getInsertPropertiesString(model: ZillowModel) -> str:
        properties = model.toProperties()
        sql = properties.getInsertWithoutDulplicateSql(["address", "property_id"])
        return sql
    if modelList is None or len(modelList) == 0:
        return []
    return [getInsertPropertiesString(model) for model in modelList]

@execSqls
@logged()
def upsertModelList(modelList: list[ZillowDetailPage]):
    def getInsertPropertiesString(model: ZillowDetailPage) -> str:
        properties = model.toProperties()
        sql = properties.getUpsertSql("property_id")
        return sql
    if modelList is None or len(modelList) == 0:
        return []
    return [getInsertPropertiesString(model) for model in modelList if model is not None]

def getModelsListFromDataset(cls):
    modelList = []
    for datasets in cls.getDataSet():
        modelList.extend([cls(*d) for d in datasets])
    return modelList

@execSqls
def updateModel(modelList: list, where_condition: list):
    return [model.getUpdateSql(where_condition) for model in modelList if model is not None]
            

if __name__ == '__main__':
    modelList = getModelsListFromDataset(Properties)
    updateModel(modelList, ["id"])