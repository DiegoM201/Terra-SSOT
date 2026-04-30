from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class TileType(str, Enum):
    WATER = "Water"
    LAND = "Land"
    HIGH_PEAK = "High Peak"
    CAVE_MOUTH = "Cave Mouth"
    FLOATING_ISLAND = "Floating Island"
    CAVERN_PATH = "Cavern Path"
    SOLID_ROCK = "Solid Rock"

class TileProperty(str, Enum):
    SHADOWED = "Shadowed"

class Tile(BaseModel):
    type: TileType
    properties: List[TileProperty] = Field(default_factory=list)

class Layer(BaseModel):
    z: int
    tiles: Dict[str, Tile] # Key is "q,r"

class GameMetadata(BaseModel):
    name: str
    version: str
    turn: int
    active_tribe: str

class Unit(BaseModel):
    id: str
    type: str
    hp: int
    max_hp: int
    atk: int
    def_stat: int = Field(alias="def")
    owner: str
    rank: int = 0
    q: int
    r: int
    z: int

    class Config:
        populate_by_name = True

class City(BaseModel):
    id: str
    owner: str
    population: int
    level: int
    q: int
    r: int
    z: int
    boundary_radius: int = 1

class TribeResources(BaseModel):
    stars: int = 5
    faith: int = 0

class Tribe(BaseModel):
    score: int = 0
    techs: List[str] = Field(default_factory=list)
    resources: TribeResources = Field(default_factory=TribeResources)

class GameState(BaseModel):
    game_metadata: GameMetadata
    layers: Dict[str, Layer] # Key is "sky", "crust", "mantle"
    units: Dict[str, Unit]
    cities: Dict[str, City]
    tribes: Dict[str, Tribe]
