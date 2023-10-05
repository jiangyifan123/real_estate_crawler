import os
import unittest
import Models
import json
import ZillowDao

class TestModel(unittest.TestCase):
    def test_ZillowModel(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/ZillowModelSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            model = Models.ZillowModel.from_json(data)
            # properties = model.toProperties()

    def test_SearchResponse(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/SearchResultSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            Models.SearchResponse.from_json(data)
    
    def test_DetailModel(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/test.json")
        with open(jsFile, "r") as f:
            data = f.read()
            o = json.loads(data)
            models = Models.ZillowDetailPage.from_json(data)

if __name__ == '__main__':
    unittest.main()