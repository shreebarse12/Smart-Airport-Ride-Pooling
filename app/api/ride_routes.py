from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.ride_service import RideService
from app.schemas.ride import RideRequestCreate, RideResponse


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rides/request", response_model=RideResponse)
def create_ride(request: RideRequestCreate, db: Session = Depends(get_db)):
    return RideService.create_ride_request(db, request.dict())



@router.post("/rides/{ride_request_id}/cancel")
def cancel_ride(ride_request_id: int, db: Session = Depends(get_db)):
    return RideService.cancel_ride(db, ride_request_id)



