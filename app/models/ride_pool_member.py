from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class RidePoolMember(Base):
    __tablename__ = "ride_pool_members"

    ride_pool_id = Column(Integer, ForeignKey("ride_pools.id"), primary_key=True)
    ride_request_id = Column(Integer, ForeignKey("ride_requests.id"), primary_key=True)
