from typing import List
from database.postgres_db import SessionLocal
import hashlib
from sqlalchemy.dialects import postgresql
from models.models.database.property_info import PropertyInfo as PropertyInfoModelDB


def get_property_by_id(property_id: str) -> PropertyInfoModelDB:
    db = next(get_postgres_db())
    return (
        db.query(PropertyInfoModelDB)
        .filter(PropertyInfoModelDB.property_id == property_id)
        .first()
    )


def get_properties_page(page_num=0, page_size=50) -> List[PropertyInfoModelDB]:
    db = next(get_postgres_db())
    return db.query(PropertyInfoModelDB).offset(page_num * page_size).limit(page_size)


def get_all_property() -> List[PropertyInfoModelDB]:
    db = next(get_postgres_db())
    return db.query(PropertyInfoModelDB).all()


def get_property(property_id=0):
    property = get_property_by_id(property_id=property_id)
    return property


def upsert_property(
    property_info_db_model: PropertyInfoModelDB
) -> PropertyInfoModelDB:
    db = next(get_postgres_db())
    # if not, create new property
    
    property_info_db_model.property_id = hashID(property_info_db_model)

    property_dict = dict(property_info_db_model.__dict__)
    property_dict.pop('_sa_instance_state', None)
    property_dict.pop('id', None)
    stmt = postgresql.insert(PropertyInfoModelDB).values(**property_dict)
    stmt = stmt.on_conflict_do_update(
        index_elements=["property_id",],
        set_=property_dict
    )
    r = db.execute(stmt)
    db.commit()
    print(f"id: {property_info_db_model.property_id} row: {r.rowcount}")
    return property_info_db_model


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hashID(model: PropertyInfoModelDB):
    return hashlib.sha256((model.address + model.city + model.state + str(model.zipcode) + model.property_type).encode('utf-8')).hexdigest()