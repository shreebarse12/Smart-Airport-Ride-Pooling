class PricingStrategy:

    BASE_FARE = 100
    PER_KM_RATE = 15
    DETOUR_RATE = 5
    POOL_DISCOUNT = 0.2

    @staticmethod
    def calculate(distance_km, detour_km=0, surge=1.0):
        base = PricingStrategy.BASE_FARE
        distance_cost = distance_km * PricingStrategy.PER_KM_RATE
        detour_cost = detour_km * PricingStrategy.DETOUR_RATE

        total = (base + distance_cost + detour_cost) * surge
        return round(total * (1 - PricingStrategy.POOL_DISCOUNT), 2)
