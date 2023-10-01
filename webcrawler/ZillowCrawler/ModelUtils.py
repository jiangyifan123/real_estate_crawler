from Models import ZillowModel, Properties

def toProperties(model):
    if isinstance(model, ZillowModel):
        homeInfo = model.hdpData.homeInfo
        return Properties(
            property_id = model.zpid,
            address = homeInfo.streetAddress,
            city = homeInfo.city,
            state = homeInfo.state,
            zipcode = homeInfo.zipcode,
            property_type = homeInfo.homeType,
            num_beds = homeInfo.bedrooms,
            num_baths = homeInfo.bathrooms,
            sq_ft = homeInfo.livingArea,
            sq_ft_lot = homeInfo.livingArea,
            purchase_price = int(homeInfo.price) if homeInfo.price is not None else homeInfo.price,
            num_days_on_market = None,
            year_built = None,
            num_garage = None,
            description = None,
            image_links = [p.url for p in model.carouselPhotos] if model.carouselPhotos is not None else [],
            schools = None,
            hoa = None,
            source = "zillow",
            zestimate = int(homeInfo.zestimate) if homeInfo.zestimate is not None else homeInfo.zestimate,
            detailurl = model.detailUrl,
            unit = homeInfo.unit,
            latitude = homeInfo.latitude,
            longitude = homeInfo.longitude
        )
    return property_id

if __name__ == "__main__":
    pass