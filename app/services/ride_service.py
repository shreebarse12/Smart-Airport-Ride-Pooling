from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.ride_request import RideRequest
from app.models.ride_pool import RidePool
from app.models.ride_pool_member import RidePoolMember
from app.matching_engine.engine import MatchingEngine
from app.services.pricing import PricingStrategy
from app.utils.distance import haversine



import logging
logger = logging.getLogger(__name__)

class RideService:


    @staticmethod
    def create_ride_request(db: Session, request_data):
        logger.info(f"Creating ride request for user {request_data.get('user_id')}")

        ride_request = RideRequest(**request_data)
        db.add(ride_request)
        db.commit()
        db.refresh(ride_request)

        pool = MatchingEngine.find_matching_pool(db, ride_request)


        if pool:
            # 🔒 Lock row to prevent overbooking
            locked_pool = db.execute(
                select(RidePool)
                .where(RidePool.id == pool.id)
                .with_for_update()
            ).scalar_one()

            if locked_pool.available_seats > 0 and \
               locked_pool.available_luggage >= ride_request.luggage_count:
            
                locked_pool.available_seats -= 1
                locked_pool.available_luggage -= ride_request.luggage_count

                member = RidePoolMember(
                    ride_pool_id=locked_pool.id,
                    ride_request_id=ride_request.id
                )

                db.add(member)
                db.commit()

                distance = haversine(
                    ride_request.pickup_lat,
                    ride_request.pickup_lng,
                    ride_request.drop_lat,
                    ride_request.drop_lng
                )

                price = PricingStrategy.calculate(distance)

                return {
                    "ride_pool_id": locked_pool.id,
                    "estimated_price": price,
                    "status": "matched"
                }

        # If no pool found → create new pool
        new_pool = RidePool()
        db.add(new_pool)
        db.commit()
        db.refresh(new_pool)

        member = RidePoolMember(
            ride_pool_id=new_pool.id,
            ride_request_id=ride_request.id
        )

        new_pool.available_seats -= 1
        new_pool.available_luggage -= ride_request.luggage_count

        db.add(member)
        db.commit()

        distance = haversine(
            ride_request.pickup_lat,
            ride_request.pickup_lng,
            ride_request.drop_lat,
            ride_request.drop_lng
        )

        price = PricingStrategy.calculate(distance)

        return {
            "ride_pool_id": new_pool.id,
            "estimated_price": price,
            "status": "new_pool_created"
        }
    @staticmethod
    def cancel_ride(db: Session, ride_request_id: int):
        logger.info(f"Cancelling ride request {ride_request_id}")

        ride_request = db.query(RideRequest)\
            .filter(RideRequest.id == ride_request_id)\
            .first()

        if not ride_request:
            return {"message": "Ride request not found"}

        member = db.query(RidePoolMember)\
            .filter(RidePoolMember.ride_request_id == ride_request_id)\
            .first()

        if member:
            locked_pool = db.execute(
                select(RidePool)
                .where(RidePool.id == member.ride_pool_id)
                .with_for_update()
            ).scalar_one()

            locked_pool.available_seats += 1
            locked_pool.available_luggage += ride_request.luggage_count

            db.delete(member)

        ride_request.status = "cancelled"
        db.commit()

        return {"status": "cancelled"}
