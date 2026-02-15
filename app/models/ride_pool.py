from sqlalchemy import Column, Float, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class RidePool(Base):
    __tablename__ = "ride_pools"

    id = Column(Integer, primary_key=True, index=True)
    total_seats = Column(Integer, default=4)
    available_seats = Column(Integer, default=4)
    total_luggage = Column(Integer, default=3)
    available_luggage = Column(Integer, default=3)
    route_distance = Column(Float, default=0)
    status = Column(String, index=True, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.total_seats is None:
            self.total_seats = 4
        if self.available_seats is None:
            self.available_seats = 4
        if self.total_luggage is None:
            self.total_luggage = 3
        if self.available_luggage is None:
            self.available_luggage = 3
        if self.route_distance is None:
            self.route_distance = 0
