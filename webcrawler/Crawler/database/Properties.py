import requests
from database.model.PropertyModel import PropertyModel
from Settings import Settings
from dataclasses import asdict
import json

URL = Settings().getConfig("database").get("url")

def updateProperty(model: PropertyModel):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request(
        method="POST",
        url=f"{URL}/properties/update",
        headers=headers,
        data=json.dumps(asdict(model))
    )
    if response.status_code == 500:
        print(f'{model.property_id} is dulplicate, update fail')
    elif response.status_code == 200:
        print(f'{model.property_id} updated successfully')
    else:
        print(f'{response.text} update fail')