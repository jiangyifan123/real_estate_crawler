from dataclasses import asdict
from dataclass_wizard import JSONWizard
from BaseDecorator import fetchSql, execSqls

class CustomJSONWizard(JSONWizard):
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
      return {k: handleValues(v).strip() for k, v in asdict(self).items() if self.canHandle(k)}
    
    def getInsertSql(self):
      sqlDict = self.__toSqlDict()
      return """INSERT INTO "{tableName}"{keys} values{values};""".format(
          tableName = self.tableName(),
          keys = "({})".format(",".join(sqlDict.keys())),
          values = "({})".format(",".join(sqlDict.values())),
      )
    
    def getInsertWithoutDulplicateSql(self, dulKeyList):
      sqlDict = self.__toSqlDict()
      return """INSERT INTO {tableName} {keys} SELECT {values} WHERE NOT EXISTS (SELECT {dulKeyList} from {tableName} where ({where_condition}));""".format(
          tableName = '"{}"'.format(self.tableName()),
          keys = "({})".format(",".join(sqlDict.keys())),
          values = "{}".format(",".join(sqlDict.values())),
          dulKeyList = ",".join(dulKeyList),
          where_condition = " OR ".join(["{}={}".format(dulKey, sqlDict.get(dulKey, 'NULL')) for dulKey in dulKeyList])
      )
    
    @classmethod
    def tableName(self):
      return ""

    @classmethod
    @fetchSql
    def getDataSet(self):
      return """SELECT * FROM "{}";""".format(self.tableName()) 

    @classmethod
    def canHandle(self, k):
      return True