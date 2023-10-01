from dataclasses import asdict

class ModelSqlsUtls(object):
    def __init__(self, model):
      self.__model = model

    def __toSqlDict(self) -> dict:
      def handleValues(v):
          if v is None:
              return "NULL"
          if isinstance(v, list):
              return r"'{0}'".format(str(v).replace('[', '{').replace(']', '}').replace("'", '"'))
          return r'{quote}{value}{quote}'.format(
              quote = "'" if isinstance(v, str) else "",
              value = str(v)
          )
      return {k: handleValues(v).strip() for k, v in asdict(self.__model).items()}
    
    def getInsertSql(self, tableName):
      sqlDict = self.__toSqlDict()
      return """INSERT INTO "{tableName}"{keys} values{values};""".format(
          tableName = tableName,
          keys = "({})".format(",".join(sqlDict.keys())),
          values = "({})".format(",".join(sqlDict.values())),
      )
    
    def getInsertWithoutDulplicateSql(self, tableName, dulKeyList):
      sqlDict = self.__toSqlDict()
      return """INSERT INTO {tableName} {keys} SELECT {values} WHERE NOT EXISTS (SELECT {dulKeyList} from {tableName} where ({where_condition}));""".format(
          tableName = '"{}"'.format(tableName),
          keys = "({})".format(",".join(sqlDict.keys())),
          values = "{}".format(",".join(sqlDict.values())),
          dulKeyList = ",".join(dulKeyList),
          where_condition = " OR ".join(["{}={}".format(dulKey, sqlDict.get(dulKey, 'NULL')) for dulKey in dulKeyList])
      )