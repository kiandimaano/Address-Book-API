from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime

class AddressBase(BaseModel):
    """shared fields and validation logic for addresses"""
    street: str
    city: str
    state: str
    country: str
    postal_code: Optional[str] = None
    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_longitude(cls, v:float) -> float:
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class AddressCreate(AddressBase):
    """validate address creation payloads"""
    pass


class AddressUpdate(BaseModel):
    """partial address updates"""
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("latitude")
    @classmethod
    def validate_longitude(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v

class AddressResponse(AddressBase):
    """structured database API responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True} # allow pydantic to read ORM models directly

class NearbyRequest(BaseModel):
    """radius-based proximity searches"""
    latitude: float
    longitude: float
    distance_km: float

    @field_validator("distance_km")
    @classmethod
    def validate_distance(cls, v):
        if v <= 0:
            raise ValueError("Distance must be greater than 0")
        return v