from database import models
from database import schemas
from typing import List
from database.postgres_db import SessionLocal
import hashlib

def update_properties(
    property_infos: List[models.PropertyInfo]
) -> List[models.PropertyInfo]:
    db = next(get_postgres_db())
    db_property_infos = []
    for property_info_model in property_infos:
        db_property = p_PropertyInfo_pydantic_to_schema(property_info_model)

        db_property_infos.append(db_property)

    db.add_all(db_property_infos)
    db.commit()
    db.refresh(db_property_infos)

    return db_property_infos


def update_property(
    property_info_model: models.PropertyInfo
) -> models.PropertyInfo:
    db = next(get_postgres_db())
    # if not, create new property
    db_property = p_PropertyInfo_pydantic_to_schema(property_info_model)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)

    return db_property


def get_postgres_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def p_PropertyInfo_pydantic_to_schema(
    model: models.PropertyInfo,
) -> schemas.PropertyInfo:
    db_property = schemas.PropertyInfo(
        property_id=hashID(model),
        address=model.address,
        city=model.city,
        state=model.state,
        zipcode=model.zipcode,
        property_type=model.property_type,
        num_beds=model.num_beds,
        num_baths=model.num_baths,
        sq_ft=model.sq_ft,
        sq_ft_lot=model.sq_ft_lot,
        purchase_price=model.purchase_price,
        num_days_on_market=model.num_days_on_market,
        year_built=model.year_built,
        num_garage=model.num_garage,
        description=model.description,
        image_links=model.image_links,
        schools=model.schools,
        hoa=model.hoa,
        source=model.source,
        zestimate=model.zestimate,
        detailurl=model.detailurl,
        unit=model.unit,
        latitude=model.latitude,
        longitude=model.longitude,
        status_text=model.status_text,
        status_type=model.status_type,
        rent_zestimate=model.rent_zestimate
    )
    return db_property

def hashID(model):
    return hashlib.sha256((model.address + model.city + model.state + str(model.zipcode) + model.property_type).encode('utf-8')).hexdigest()