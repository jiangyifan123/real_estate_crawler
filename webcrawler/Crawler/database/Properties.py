import requests
from database.model.PropertyModel import PropertyModel
from Settings import Settings

URL = Settings().getConfig("database").get("url")

def updateProperty(model: PropertyModel):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request(
        method="POST",
        url=f"{URL}/properties/property",
        headers=headers,
        data=model.to_json()
    )
    print(response.text)