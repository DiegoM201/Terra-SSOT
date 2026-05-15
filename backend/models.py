from pydantic import BaseModel, Field, ConfigDict

class Tile(BaseModel):
    q: int
    r: int
    z: int
    biome: str
    resource: str | None = None
    building: str | None = None

class Unit(BaseModel):
    id: str
    type: str
    tribe: str
    hp: int
    max_hp: int
    atk: int
    def_stat: int = Field(..., alias="def")
    q: int
    r: int
    z: int
    is_veteran: bool = False
    range: int = 1
    kills: int = 0
    has_attacked: bool = False
    model_config = ConfigDict(populate_by_name=True)

class City(BaseModel):
    id: str
    name: str
    tribe: str
    q: int
    r: int
    z: int
    level: int
    population: int
    max_population: int

class TribeHeuristics(BaseModel):
    expansion_weight: float = 0.5
    aggression_weight: float = 0.5
    faith_weight: float = 0.5

class Player(BaseModel):
    tribe: str
    stars: int
    techs: list[str] = Field(default_factory=list)
    total_cities: int
    heuristics: TribeHeuristics = Field(default_factory=TribeHeuristics)

class GameState(BaseModel):
    turn: int
    tiles: dict[str, Tile]
    units: dict[str, Unit]
    cities: dict[str, City]
    players: dict[str, Player]
