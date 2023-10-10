from dataclasses import asdict, is_dataclass
from dataclass_wizard import JSONWizard
from BaseDecorator import fetchSql, execSqls
from enum import Enum
import json

class CustomJSONWizard(JSONWizard):
  class EnterFrom(Enum):
    READ = 1
    WRITE = 2
    UPDATE = 3
  
  def __post_init__(self):
    self.toModelDict = {}

  def handleValues(self, k, v):
    if v is None:
      return "NULL"
    if isinstance(v, list) or isinstance(v, dict):
      return "'{}'".format(json.dumps(v).replace("[", "{").replace("]", "}"))
    if isinstance(v, str):
      return r"'{value}'".format(
        value = str(v).replace(r"'", r"''")
      )
    return str(v)

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
  
  def registerModelFactory(self, cls, fun):
    if callable(fun):
      self.toModelDict[cls] = fun
  
  def getModelFactory(self, cls):
    def defaultFactory():
      return None
    return self.toModelDict.get(cls, defaultFactory)()