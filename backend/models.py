from pydantic import BaseModel, Field
from typing import List, Optional

class Unit(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the unit")
    max_hp: int = Field(..., ge=1, le=40, description="Maximum HP (1-40)")
    attack: int = Field(..., ge=1, le=40, description="Attack stat (1-40)")
    defense: int = Field(..., ge=1, le=40, description="Defense stat (1-40)")
    range: int = Field(1, ge=1, description="Attack range (defaults to 1 for melee)")
    traits: List[str] = Field(default_factory=list, description="Special traits (e.g., Sky-native, Flyer)")

class Tribe(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the tribe")
    home_layer: int = Field(..., ge=-1, le=1, description="Starting layer: -1 (Mantle), 0 (Surface), 1 (Heavens)")
    feature: str = Field(..., min_length=1, description="Unique tribe feature")
    starting_tech: str = Field(..., min_length=1, description="Starting Tier 1 technology")
