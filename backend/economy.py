from backend.models import GameState

def calculate_spt(state: GameState, tribe: str) -> int:
    """
    Calculates the Stars Per Turn (SPT) for a given tribe.
    Base SPT is 2. Each city adds its level to the SPT.
    """
    base_spt = 2
    city_spt = sum(city.level for city in state.cities.values() if city.tribe == tribe)
    return base_spt + city_spt

def calculate_tech_cost(base_cost: int, total_cities: int, multiplier: int = 2) -> int:
    """
    Calculates the inflated cost of a technology based on the number of cities owned.
    Formula: Base_Cost + (Total_Cities * Multiplier)
    """
    return base_cost + (total_cities * multiplier)
