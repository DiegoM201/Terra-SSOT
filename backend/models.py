from pydantic import BaseModel, Field
from typing import List

class Unit(BaseModel):
    id: str
    name: str
    max_hp: int = Field(ge=1, le=40, description="HP must be between 1 and 40")
    attack: int = Field(ge=1, le=5)
    defense: int = Field(ge=1, le=5)
    movement: int = Field(ge=1, le=3)
    range: int = Field(ge=1, le=3)
    traits: List[str]

class Tribe(BaseModel):
    id: str
    name: str
    home_layer: int = Field(ge=-1, le=1, description="Z-axis: -1 (Mantle), 0 (Surface), 1 (Sky)")
    starting_tech: str
    passive_feature: str
