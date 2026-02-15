from pydantic import BaseModel, Field

class RideRequestCreate(BaseModel):
    user_id: int
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float
    luggage_count: int = Field(ge=0)
    detour_tolerance_km: float = Field(ge=0)

class RideResponse(BaseModel):
    ride_pool_id: int
    estimated_price: float
    status: str
