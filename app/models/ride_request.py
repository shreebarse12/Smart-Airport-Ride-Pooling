from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    drop_lat = Column(Float)
    drop_lng = Column(Float)
    luggage_count = Column(Integer)
    detour_tolerance_km = Column(Float)
    #status = Column(String, index=True, default="pending")
    #created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, index=True, default="pending")
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
