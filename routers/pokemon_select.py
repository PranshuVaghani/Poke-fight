# This file includes endpoints for selecting a pokemon and its moves , displaying pokemon's stats
# and also includes the endpoints for displaying all the pokemon and all the moves a selected pokemon can learn.

from fastapi import FastAPI, status, APIRouter, HTTPException, Depends, Body
from sqlmodel import Session
import schemas.schemas_pokemon as schemas_pokemon, models
from database import get_db
import oauth2

router = APIRouter(
    prefix="/pokemon",
    tags=["pokemon"]
)


# Endpoint for de-selecting the pokemon.
@router.delete("/deselect", status_code=200)
def deselect_pokemon(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    entry = db.query(models.SelectedPokemon).filter(models.SelectedPokemon.user_id == get_current_user.id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="No Pokémon selected")

    db.delete(entry)
    db.commit()
    return {"message": "Pokémon deselected successfully."}


# Endpoint for getting/ checking all the pokemon.
@router.get("/all",response_model=list[schemas_pokemon.pokemon_all],status_code=status.HTTP_202_ACCEPTED)
def all_pokemon(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    pokemons = db.query(models.Pokemon).all()
    return pokemons


# Endpoint for selecting a pokemon.
# Takes integer and string.
@router.post("/select/{name}",status_code=status.HTTP_202_ACCEPTED)
def see_pokemon(name: str , db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    pokemon_see_output = db.query(models.Pokemon).filter(models.Pokemon.name == name.capitalize()).first()

    if not pokemon_see_output:
        pokemon_see_output = db.query(models.Pokemon).filter(models.Pokemon.id == int(name)).first()

        if not pokemon_see_output:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} doesn't exist in the database")
    
    existing = db.query(models.SelectedPokemon).filter(models.SelectedPokemon.user_id == get_current_user.id).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You have already selected a pokemon")
    
    
    selected_entry = models.SelectedPokemon(
        user_id = get_current_user.id,

        pokemon_id = pokemon_see_output.id,
        pokemon_name = pokemon_see_output.name,
        type_1 = pokemon_see_output.type_1,
        type_2 = pokemon_see_output.type_2,
        hp = pokemon_see_output.hp,
        attack = pokemon_see_output.attack,
        defense = pokemon_see_output.defense,
        sp_atk = pokemon_see_output.sp_atk,
        sp_def = pokemon_see_output.sp_def,
        speed = pokemon_see_output.speed,
        turn = False
    )

    db.add(selected_entry)
    db.commit()
    db.refresh(selected_entry)
    
    return {"message": f"{pokemon_see_output.name} selected. Now choose your moves."}


# Endpoint for selecting moves for the selected pokemon.
@router.post("/select-moves", status_code=status.HTTP_200_OK)
def choose_moves(
    payload: schemas_pokemon.PokemonSelectRequest,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user)
):
    selected = db.query(models.SelectedPokemon).filter_by(user_id=get_current_user.id).first()
    if not selected:
        raise HTTPException(status_code=404, detail="You have not selected a Pokémon yet.")

    pokemon = db.query(models.Pokemon).filter_by(id=selected.pokemon_id).first()
    allowed_move_ids = {move.id for move in pokemon.moves}

    if payload.move_1_id not in allowed_move_ids or payload.move_2_id not in allowed_move_ids:
        raise HTTPException(status_code=400, detail="Invalid move(s) for the selected Pokémon.")

    selected.move_1_id = payload.move_1_id
    selected.move_2_id = payload.move_2_id
    db.commit()
    return {"message": "Moves selected successfully!"}


# Endpoint for getting all the moves the selected pokemon can learn.
@router.get("/moves/{pokemon_name}", response_model=list[schemas_pokemon.Move])
def get_pokemon_moves(pokemon_name: str, db: Session = Depends(get_db)):
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.name == pokemon_name).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    moves = (
        db.query(models.Move)
        .join(models.PokemonMove, models.Move.id == models.PokemonMove.move_id)
        .filter(models.PokemonMove.pokemon_id == pokemon.id)
        .all()
    )
    return moves



# Endpoint for getting stats of a pokemon.
# Takes integer and string.
@router.post("/info/{name}",status_code=status.HTTP_302_FOUND,response_model=schemas_pokemon.pokemon_display)
def see_pokemon(name: str , db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    pokemon_see_output = db.query(models.Pokemon).filter(models.Pokemon.name == name).first()

    if not pokemon_see_output:
        pokemon_see_output = db.query(models.Pokemon).filter(models.Pokemon.id == int(name)).first()

        if not pokemon_see_output:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{name} doesn't exist in the database")
    
    return pokemon_see_output