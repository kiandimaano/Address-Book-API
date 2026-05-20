import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=schemas.AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """create new address record"""
    logger.info("POST /addresses called")
    return crud.create_address(db, address)

@router.get("/", response_model=List[schemas.AddressResponse])
def list_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """retrieve paginated list of all addresses"""
    logger.info(f"GET /addresses called (skip={skip}, limit={limit})")
    return crud.get_all_addresses(db, skip, limit)

@router.get("/{address_id}", response_model=schemas.AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    """retrieve specific address by its ID"""
    logger.info(f"GET /addresses/{address_id} called")
    address = crud.get_address(db, address_id)
    if not address:
        logger.warning(f"Address {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=schemas.AddressResponse)
def update_address(address_id: int, updates: schemas.AddressUpdate, db: Session = Depends(get_db)):
    """partially update existing address by ID"""
    logger.info(f"PUT /addresses/{address_id} called")
    address = crud.update_address(db, address_id, updates)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """delete address by ID"""
    logger.info(f"DELETE /addresses/{address_id} called")
    deleted = crud.delete_address(db, address_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Address not found")

@router.get("/nearby/search", response_model=List[schemas.AddressResponse])
def get_nearby(
    latitude: float,
    longitude: float,
    distance_km: float,
    db: Session = Depends(get_db)
):
    logger.info(f"GET /addresses/nearby/search called: ({latitude}, {longitude}), {distance_km}km")
    return crud.get_nearby_addresses(db, latitude, longitude, distance_km)