import psycopg2
from Models import ZillowModel
from datetime import date
from functools import wraps
import traceback
from CustomLog import logged
import ModelUtils
import SqlUtls

host = "100.87.56.32"
user = "nimbus_nova"
password = "nimbus_nova"
port = "5432"
database = "real_estate_app"

RAW_PROPERTIES = "raw.properties"



def getConn():
    return psycopg2.connect(database=database,
                            host=host,
                            user=user,
                            password=password,
                            port=port)

"""
write a list of sqls
"""
def execSqls(fun):
    @wraps(fun)
    def decorator(*args, **kargs):
        conn = getConn()
        try:
            with conn.cursor() as curs:
                for sql in fun(*args, **kargs):
                    curs.execute(sql)
                conn.commit()
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            if conn:
                conn.close()
    return decorator

"""
read sql
"""
def fetchSql(fun):
    @wraps(fun)
    def decorator(*args, **kargs):
        conn = getConn()
        try:
            with conn.cursor() as curs:
                sql = fun(*args, **kargs)
                curs.execute(sql)
                return curs.fetchall()
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            if conn:
                conn.close()
    return decorator

@fetchSql
@logged()
def getTables():
    return """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""

def getInsertPropertiesString(model: ZillowModel) -> str:
    properties = ModelUtils.toProperties(model)
    sql = SqlUtls.ModelSqlsUtls(properties).getInsertWithoutDulplicateSql(RAW_PROPERTIES, ["address", "property_id"])
    return sql

@execSqls
@logged()
def insertModelList(modelList: list[ZillowModel]):
    if modelList is None or len(modelList) == 0:
        return []
    return [getInsertPropertiesString(model) for model in modelList]
            

if __name__ == '__main__':
    pass