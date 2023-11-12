from database import models
from database import schemas
from typing import List
from database.postgres_db import SessionLocal
import hashlib
from sqlalchemy.dialects.postgresql import insert

def upsert_property(
    property_info_model: models.PropertyInfo
) -> models.PropertyInfo:
    db = next(get_postgres_db())
    # if not, create new property
    
    property_info_model.property_id = hashID(property_info_model)
    property_dict = property_info_model.dict()
    stmt = insert(schemas.PropertyInfo).values([property_dict,])
    stmt = stmt.on_conflict_do_update(
        index_elements=["property_id",],
        set_=property_dict
    )
    r = db.execute(stmt)
    print(f'{property_info_model.property_id} result: {r.rowcount}')
    return property_info_model


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hashID(model):
    return hashlib.sha256((model.address + model.city + model.state + str(model.zipcode) + model.property_type).encode('utf-8')).hexdigest()