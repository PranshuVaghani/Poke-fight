# Schematics of the battle endpoint.

from pydantic import BaseModel, EmailStr
from typing import Optional

class start(BaseModel):
    pokemon_name: str
    type_1: str
    type_2: Optional[str]
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int

    move_1: str
    move_2: str

    class Config:
        from_attributes = True

class fight(BaseModel):
    pokemon_name: str
    type_1: str
    type_2: Optional[str]

    hp:int
    attack:int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int

    lost_hp: int

    move_1: str
    move_2: str

class MoveChoice(BaseModel):
    move: str