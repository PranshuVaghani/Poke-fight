# Schematic for pokemon endpoint.

from typing import Optional
from pydantic import BaseModel


class pokemon_all(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class pokemon_display(BaseModel):
    id: int
    name: str
    type_1: str
    type_2: Optional[str]
    total: int
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int
    generation: int

class PokemonSelectRequest(BaseModel):
    move_1_id: int
    move_2_id: int

class Move(BaseModel):
    id: int
    name: str
    power: int | None
    type: str | None
    accuracy: int | None

    class Config:
        orm_mode = True