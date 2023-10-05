from dataclasses import asdict
from dataclass_wizard import JSONWizard
from BaseDecorator import fetchSql, execSqls
from enum import Enum

class CustomJSONWizard(JSONWizard):
  class EnterFrom(Enum):
    READ = 1
    WRITE = 2
    UPDATE = 3

  def handleValues(self, k, v):
    if v is None:
      return "NULL"
    if isinstance(v, list):
      return r"'{0}'".format(str(v).replace('[', '{').replace(']', '}').replace("'", '"'))
    return r'{quote}{value}{quote}'.format(
      quote = "'" if isinstance(v, str) else "",
      value = str(v).replace(r"'", r"''") if isinstance(v, str) else str(v)
    )

  def _toSqlDict(self, enterFrom) -> dict:
    return {k: self.handleValues(k, v).strip() for k, v in asdict(self).items() if self.canHandle(k, enterFrom)}
  
  def getInsertSql(self):
    sqlDict = self._toSqlDict(self.EnterFrom.WRITE)
    return """INSERT INTO "{tableName}"{keys} values{values};""".format(
        tableName = self.tableName(),
        keys = "({})".format(",".join(sqlDict.keys())),
        values = "({})".format(",".join(sqlDict.values())),
    )
  
  def getInsertWithoutDulplicateSql(self, dulKeyList):
    sqlDict = self._toSqlDict(self.EnterFrom.WRITE)
    return """INSERT INTO {tableName} {keys} SELECT {values} WHERE NOT EXISTS (SELECT {dulKeyList} from {tableName} where ({where_condition}));""".format(
        tableName = '"{}"'.format(self.tableName()),
        keys = "({})".format(",".join(sqlDict.keys())),
        values = "{}".format(",".join(sqlDict.values())),
        dulKeyList = ",".join(dulKeyList),
        where_condition = " OR ".join(["{}={}".format(dulKey, sqlDict.get(dulKey, 'NULL')) for dulKey in dulKeyList])
    )
  
  def getUpsertSql(self, conflict):
    sqlDict = self._toSqlDict(self.EnterFrom.WRITE)
    return """
INSERT INTO "{tableName}" {keys}
VALUES {values}
ON CONFLICT ("{conflict}")
DO UPDATE SET {set_values};
    """.format(
      tableName = self.tableName(),
      keys = "({})".format(",".join(sqlDict.keys())),
      values = "({})".format(",".join(sqlDict.values())),
      conflict = conflict,
      set_values = ','.join(['"{key}"=EXCLUDED."{key}"'.format(key=k) for k in sqlDict.keys() if k != conflict]),
    )
  
  def getUpdateSql(self, conditionKeyList):
    sqlDict = self._toSqlDict(self.EnterFrom.UPDATE)
    return """
UPDATE "raw.properties" 
SET {values}
WHERE
{where_condition};""".format(
      values = ','.join([""""{}"={}""".format(k, v) for k, v in sqlDict.items()]),
      where_condition = " AND ".join([""""{}"={}""".format(k, sqlDict.get(k, sqlDict[k])) for k in conditionKeyList])
    )
  
  @classmethod
  def tableName(self):
    return ""

  @classmethod
  @fetchSql
  def getDataSet(self):
    return """SELECT * FROM "{}";""".format(self.tableName()) 

  @classmethod
  def canHandle(self, k, enterFrom):
    return True