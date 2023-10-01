import os
import unittest
from Models import ZillowModel, SearchResponse
from ModelUtils import toProperties
from SqlUtls import ModelSqlsUtls

class TestModel(unittest.TestCase):
    def test_ZillowModel(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/ZillowModelSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            model = ZillowModel.from_json(data)
            properties = ModelSqlsUtls(toProperties(model))
            with open("test", "w") as f:
                f.write(properties.getInsertWithoutDulplicateSql("raw.properties", ["address", "property_id"]))
                # f.write(properties.getInsertSql("raw.properties"))

    def test_SearchResponse(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/SearchResultSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            SearchResponse.from_json(data)

if __name__ == '__main__':
    unittest.main()