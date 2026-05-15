from pydantic import BaseModel, Field

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

class GameState(BaseModel):
    turn: int
    tiles: dict[str, Tile]
    units: dict[str, Unit]
    cities: dict[str, City]
