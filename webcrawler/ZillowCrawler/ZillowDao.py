import psycopg2
from ZillowModel import ZillowModel
from datetime import date
import unittest
import os
from functools import wraps
import traceback

host = "100.87.56.32"
user = "nimbus_nova"
password = "nimbus_nova"
port = "5432"
database = "real_estate_app"

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
def getTables():
    return """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""

def safeFormat(sql: str, values: dict) -> str:
    safeValues = {k: (v or 'NULL') for k, v in values.items()}
    return sql.format(**safeValues)

def getInsertPropertiesString(model: ZillowModel) -> str:
    homeInfo = model.hdpData.homeInfo
    sql = """
    INSERT INTO properties (create_time, zpid, streetAddress, zipcode, city, state, 
    livingArea, homeType, latitude, longitude, price, bathrooms, bedrooms, homeStatus, priceForHDP, currency, country, unit,
    datePriceChanged, priceChange, taxAssessedValue, zestimate, rentZestimate, detailUrl, imgSrc) 
    SELECT '{create_time}', {zpid}, '{streetAddress}', '{zipcode}', '{city}', '{state}', {livingArea}, '{homeType}', {latitude}, {longitude}, {price}, {bathrooms}, {bedrooms}, '{homeStatus}', {priceForHDP}, '{currency}', '{country}', '{unit}', {datePriceChanged}, {priceChange},
    {taxAssessedValue}, {zestimate}, {rentZestimate}, '{detailUrl}', '{imgSrc}'
    WHERE NOT EXISTS (SELECT zpid from properties where zpid={zpid});
    """
    value = {
        'create_time': date.today(), 
        'zpid': homeInfo.zpid, 
        'streetAddress': homeInfo.streetAddress, 
        'zipcode': homeInfo.zipcode, 
        'city': homeInfo.city, 
        'state': homeInfo.state,
        'livingArea': homeInfo.livingArea, 
        'homeType': homeInfo.homeType, 
        'latitude': homeInfo.latitude, 
        'longitude': homeInfo.longitude, 
        'price': homeInfo.price, 
        'bathrooms': homeInfo.bathrooms, 
        'bedrooms': homeInfo.bedrooms, 
        'homeStatus': homeInfo.homeStatus,
        'priceForHDP': homeInfo.priceForHDP, 
        'currency': homeInfo.currency, 
        'country': homeInfo.country, 
        'unit': homeInfo.unit, 
        'datePriceChanged': homeInfo.datePriceChanged, 
        'priceChange': homeInfo.priceChange, 
        'taxAssessedValue': homeInfo.taxAssessedValue, 
        'zestimate': homeInfo.zestimate,
        'rentZestimate': homeInfo.rentZestimate, 
        'detailUrl': model.detailUrl, 
        'imgSrc': model.imgSrc
    }
    return safeFormat(sql, value)

@execSqls
def insertModelList(modelList: list[ZillowModel]):
    if modelList is None or len(modelList) == 0:
        return []
    return [getInsertPropertiesString(model) for model in modelList]

class TestDao(unittest.TestCase):
    def test_getInsertPropertiesString(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/ZillowModelSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            model = ZillowModel.from_json(data)
            sql = getInsertPropertiesString(model)
            conn = getConn()
            with conn:
                with conn.cursor() as curs:
                    curs.execute(sql)
                conn.commit()
            if conn:
                conn.close()

    def test_getTables(self):
        tableList = getTables()
        # print(tableList)
        self.assertTrue(type(tableList), list)
            

if __name__ == '__main__':
    unittest.main()