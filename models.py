# This file contains the format and the creation of database using sqlalchemy.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from database import Base


# Database of Users
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email_id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


# Creates a large database of linked moves and pokemon
class PokemonMove(Base):
    __tablename__ = "pokemon_moves"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    move_id = Column(Integer, ForeignKey("moves.id"))

    # Bi- Directional Relation-ship
    pokemon = relationship("Pokemon", back_populates="pokemon_moves")
    move = relationship("Move", back_populates="move_pokemons")


class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    type_1 = Column(String, nullable=False)
    type_2 = Column(String)
    total = Column(Integer, nullable=False)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_atk = Column(Integer)
    sp_def = Column(Integer)
    speed = Column(Integer)
    generation = Column(Integer)

    # ✅ Replaces the incorrect secondary= relationship
    pokemon_moves = relationship("PokemonMove", back_populates="pokemon", cascade="all, delete-orphan")

    # ✅ Now you can access pokemon.moves (list of Move objects) using association_proxy
    moves = association_proxy(
        "pokemon_moves",
        "move",
        creator=lambda move: PokemonMove(move=move)
    )


class SelectedPokemon(Base):
    __tablename__ = "selected_pokemon"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, nullable=False)
    pokemon_name = Column(String, nullable=False, unique=True)
    type_1 = Column(String, nullable=False)
    type_2 = Column(String)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    sp_atk = Column(Integer, nullable=False)
    sp_def = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    turn = Column(Boolean, nullable=False)

    move_1_id = Column(Integer, ForeignKey("moves.id"))
    move_2_id = Column(Integer, ForeignKey("moves.id"))

    move_1 = relationship("Move", foreign_keys=[move_1_id])
    move_2 = relationship("Move", foreign_keys=[move_2_id])

    user = relationship("Users")


class ComputerSelected(Base):
    __tablename__ = "computer_selected"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, nullable=False)
    pokemon_name = Column(String, nullable=False, unique=True)
    type_1 = Column(String, nullable=False)
    type_2 = Column(String)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    sp_atk = Column(Integer, nullable=False)
    sp_def = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    turn = Column(Boolean, nullable=False)

    move_1_id = Column(Integer, ForeignKey("moves.id"))
    move_2_id = Column(Integer, ForeignKey("moves.id"))

    move_1 = relationship("Move", foreign_keys=[move_1_id])
    move_2 = relationship("Move", foreign_keys=[move_2_id])

    user = relationship("Users")


class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    power = Column(Integer)
    accuracy = Column(Integer)
    type = Column(String)
    damage_class = Column(String)
    description = Column(String)

    # ✅ Bi-directional relationship for PokemonMove
    move_pokemons = relationship("PokemonMove", back_populates="move")
