from sqlalchemy.orm import Session
from app.models.ride_pool import RidePool
from app.models.ride_pool_member import RidePoolMember
from app.models.ride_request import RideRequest
from app.utils.distance import haversine

AIRPORT_LAT = 19.0896
AIRPORT_LNG = 72.8656

class MatchingEngine:

    @staticmethod
    def calculate_pool_route_distance(db: Session, pool_id: int):
        members = db.query(RidePoolMember)\
            .filter(RidePoolMember.ride_pool_id == pool_id)\
            .all()

        total_distance = 0
        prev_lat = AIRPORT_LAT
        prev_lng = AIRPORT_LNG

        for member in members:
            request = db.query(RideRequest)\
                .filter(RideRequest.id == member.ride_request_id)\
                .first()

            dist = haversine(prev_lat, prev_lng,
                             request.drop_lat, request.drop_lng)

            total_distance += dist
            prev_lat = request.drop_lat
            prev_lng = request.drop_lng

        return total_distance

    @staticmethod
    def find_matching_pool(db: Session, request):

        active_pools = db.query(RidePool)\
            .filter(RidePool.status == "active",
                    RidePool.available_seats > 0,
                    RidePool.available_luggage >= request.luggage_count)\
            .all()

        best_pool = None
        min_detour = float("inf")

        for pool in active_pools:

            original_distance = MatchingEngine.calculate_pool_route_distance(db, pool.id)

            # simulate adding new passenger at end
            last_drop_lat = AIRPORT_LAT
            last_drop_lng = AIRPORT_LNG

            members = db.query(RidePoolMember)\
                .filter(RidePoolMember.ride_pool_id == pool.id)\
                .all()

            if members:
                last_member = members[-1]
                last_request = db.query(RideRequest)\
                    .filter(RideRequest.id == last_member.ride_request_id)\
                    .first()

                last_drop_lat = last_request.drop_lat
                last_drop_lng = last_request.drop_lng

            new_leg = haversine(last_drop_lat, last_drop_lng,
                                request.drop_lat, request.drop_lng)

            new_distance = original_distance + new_leg
            detour = new_distance - original_distance

            if detour <= request.detour_tolerance_km:
                if detour < min_detour:
                    min_detour = detour
                    best_pool = pool

        return best_pool
