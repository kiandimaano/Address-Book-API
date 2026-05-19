import logging
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from app import models, schemas
from typing import Optional

logger = logging.getLogger(__name__)

def create_address(db: Session, address: schemas.AddressCreate) -> models.Address:
    """create a new address record in db"""
    logger.info(f"Creating address: {address.street}, {address.city}")
    db_address = models.Address(**address.model_dump())
    db.add(db_address)

    try:
        db.commit()
        db.refresh(db_address)
        logger.info(f"Address created with ID: {db_address.id}")
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create address: {e}")
        raise

def get_address(db: Session, address_id: int) -> Optional[models.Address]:
    """fetch a single address by ID"""
    logger.debug(f"Fetching address ID: {address_id}")
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_all_addresses(db: Session, skip: int = 0, limit: int = 100):
    """fetch address list with pagination support"""
    logger.debug(f"Fetching addresses: skip={skip}, limit={limit}")
    return db.query(models.Address).offset(skip).limit(limit).all()

def update_address(db: Session, address_id: int, updates: schemas.AddressUpdate) -> Optional[models.Address]:
    """partially update existing record"""
    logger.info(f"Updating address ID: {address_id}")
    db_address = get_address(db, address_id)

    if not db_address:
        logger.warning(f"Address ID {address_id} not found for update")
        return None
    
    # Extract only provided fields to avoid overwriting existing data with nulls
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_address, field, value)
    
    try:
        db.commit()
        db.refresh(db_address)
        logger.info(f"Address ID {address_id} updated successfully")
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update address ID {address_id}: {e}")
        raise

def delete_address(db: Session, address_id: int) -> bool:
    """delete address by ID"""
    logger.info(f"Deleting Address ID {address_id}")
    db_address = get_address(db, address_id)

    if not db_address:
        logger.warning(f"Address ID {address_id} not found for delete")
        return False
    
    try:
        db.delete(db_address)
        db.commit()
        logger.info(f"Address ID {address_id} deleted")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete address ID {address_id}: {e}")
        raise

def get_nearby_addresses(db: Session, lat: float, lon: float, distance_km: float):
    logger.info(f"Searching nearby addresses: ({lat}, {lon}), within {distance_km} km")
    all_addresses = db.query(models.Address).all()
    origin = (lat, lon)
    nearby = []
    for address in all_addresses:
        point = (address.latitude, address.longitude)
        dist = geodesic(origin, point).kilometers
        if dist <= distance_km:
            nearby.append(address)
    logger.info(f"Found {len(nearby)} addresses within {distance_km} km")
    return nearby

