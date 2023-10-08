import psycopg2
from functools import wraps
import traceback
from collections.abc import Iterable


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
                sqlList = fun(*args, **kargs)
                if isinstance(sqlList, Iterable):
                    for sql in sqlList:
                        try:
                            curs.execute(sql)
                        except Exception as e:
                            print(e)
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
        size = 50
        try:
            with conn.cursor() as curs:
                sql = fun(*args, **kargs)
                curs.execute(sql)
                d = curs.fetchmany(size)
                while len(d):
                    yield d
                    d = curs.fetchmany(size)
        except Exception as e:
            print(e)
            traceback.print_exc()
        finally:
            if conn:
                conn.close()
    return decorator