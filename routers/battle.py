# This file contains the endpoints for fighting / battling with the selected pokemon.
# Also includes the endpoint of computer selecting a pokemon.

from fastapi import FastAPI, APIRouter, Depends,status, HTTPException
from sqlmodel import Session
import schemas.schemas_battle as schemas_battle, models, oauth2
from database import get_db
import random 
from battle_utils import damage_delt, move_accuracy,move_type_effective

router = APIRouter(
    prefix = "/battle",
    tags = ["battle"]
)



# This endpoint randomly selects the computer's pokemon and it's moves.
@router.post("/start/computer", status_code=status.HTTP_202_ACCEPTED, response_model = schemas_battle.start)
def computer_select(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    p1_selected  = db.query(models.SelectedPokemon).filter(models.SelectedPokemon.user_id == get_current_user.id).first()

    computer_selects = db.query(models.Pokemon).filter(models.Pokemon.id == random.randint(1,721)).first()

    all_moves = computer_selects.moves
    if len(all_moves) == 0:
        raise HTTPException(status_code=500, detail="Computer Pokémon has no available moves.")

    elif len(all_moves) == 1:
        # Use the same move twice
        selected_moves = [all_moves[0], all_moves[0]]

    else:
        selected_moves = random.sample(all_moves, 2)


    #Saving computer's pokemon to DB
    existing = db.query(models.ComputerSelected).filter(models.ComputerSelected.user_id==get_current_user.id).first()
    if existing:
        db.delete(existing)
        db.commit()

    computer_entry = models.ComputerSelected(
        user_id=get_current_user.id,
        pokemon_id=computer_selects.id,
        pokemon_name=computer_selects.name,
        type_1=computer_selects.type_1,
        type_2=computer_selects.type_2,
        hp=computer_selects.hp,
        attack=computer_selects.attack,
        defense=computer_selects.defense,
        sp_atk=computer_selects.sp_atk,
        sp_def=computer_selects.sp_def,
        speed=computer_selects.speed,
        turn=False,
        move_1_id=selected_moves[0].id,
        move_2_id=selected_moves[1].id
    )

    db.add(computer_entry)
    db.commit()
    db.refresh(computer_entry)

    return {
        "pokemon_name": computer_entry.pokemon_name,
        "type_1": computer_entry.type_1,
        "type_2": computer_entry.type_2,
        "hp": computer_entry.hp,
        "attack": computer_entry.attack,
        "defense": computer_entry.defense,
        "sp_atk": computer_entry.sp_atk,
        "sp_def": computer_entry.sp_def,
        "speed": computer_entry.speed,
        "move_1": selected_moves[0].name,
        "move_2": selected_moves[1].name,
    }




# This endpoint is for fighting the computer.
# Each move is registered and it's output is given.
@router.post("/fight/computer", status_code=status.HTTP_202_ACCEPTED)
def vscomputer(move_data: schemas_battle.MoveChoice, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    move = move_data.move
    computer_pokemon = db.query(models.ComputerSelected).filter_by(user_id=get_current_user.id).first()
    user_pokemon = db.query(models.SelectedPokemon).filter_by(user_id=get_current_user.id).first()

    # This checks if the user or the computer's pokemon are not selected.
    if not computer_pokemon or not user_pokemon:
        raise HTTPException(status_code=404, detail="Battle Pokémon not found.")

    #gets the moves of the user and computer from the database.
    user_move = db.query(models.Move).filter(models.Move.name == move).first()
    computer_move = computer_pokemon.move_1 if random.randint(0, 1) == 0 else computer_pokemon.move_2

    # A boolean variable to check if computer's move landed or missed
    check_move_hit_computer = move_accuracy(computer_move.accuracy)
    if check_move_hit_computer:
        user_pokemon.hp = user_pokemon.hp - damage_delt(computer_pokemon.attack, user_pokemon.defense,computer_pokemon.sp_atk,user_pokemon.sp_def,computer_move.power, computer_move.damage_class,computer_move.type, user_pokemon.type_1, user_pokemon.type_2)
    
    # Reusing the variable to check if user's move landerd or missed
    check_move_hit_user = move_accuracy(user_move.accuracy)
    if check_move_hit_user:
        computer_pokemon.hp = computer_pokemon.hp - damage_delt(user_pokemon.attack, computer_pokemon.defense, user_pokemon.sp_atk, computer_pokemon.sp_def,user_move.power,user_move.damage_class, user_move.type, computer_pokemon.type_1, computer_pokemon.type_2)

    db.commit()

    # End's the fight if the user's pokemon is unable to battle/ pokemon faints.
    if user_pokemon.hp <= 0:

        db.delete(computer_pokemon)
        db.delete(user_pokemon)
        db.commit()       
        
        return{
            "result": "Computer has won the match",
            "hp": computer_pokemon.hp,
            "computer's pokemon": computer_pokemon.name,
            "move_used": computer_move.name   
        }
    

        
    # End's the fight if the computer's pokemon is unable to battle/ pokemon faints.
    elif computer_pokemon.hp <= 0:

        db.delete(computer_pokemon)
        db.delete(user_pokemon)
        db.commit()

        return{
            "result": "User has won the match",
            "hp": user_pokemon.hp,
            "move_used": move
        }

    # The return statement.
    return {
        "player": {
            "name": user_pokemon.pokemon_name,
            "hp": user_pokemon.hp,
            "move_used": move,
            "move_hit": check_move_hit_user
        },
        "computer": {
            "name": computer_pokemon.pokemon_name,
            "hp": computer_pokemon.hp,
            "move_used": computer_move.name,
            "move_hit": check_move_hit_computer
        }
    
    }



#online-mode
@router.post("/start/{opponent_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas_battle.start)
def start_battle(opponent_id: int , db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    p1_selected = db.query(models.SelectedPokemon).filter(models.SelectedPokemon.user_id==get_current_user.id).first()
    p2_selected = db.query(models.SelectedPokemon).filter(models.SelectedPokemon.user_id==opponent_id).first()

    