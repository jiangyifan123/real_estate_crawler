from database import schemas
from typing import List
from database.postgres_db import SessionLocal
import hashlib
from sqlalchemy.dialects.postgresql import insert
from models.models.database.property_info import PropertyInfo as PropertyInfoModelDB

def upsert_property(
    property_info_db_model: PropertyInfoModelDB
) -> PropertyInfoModelDB:
    db = next(get_postgres_db())
    # if not, create new property
    
    property_info_db_model.property_id = hashID(property_info_db_model)
    property_dict = property_info_db_model.dict()
    stmt = insert(schemas.PropertyInfo).values([property_dict,])
    stmt = stmt.on_conflict_do_update(
        index_elements=["property_id",],
        set_=property_dict
    )
    db.execute(stmt)
    print(property_info_db_model)
    return property_info_db_model


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hashID(model: PropertyInfoModelDB):
    return hashlib.sha256((model.address + model.city + model.state + str(model.zipcode) + model.property_type).encode('utf-8')).hexdigest()