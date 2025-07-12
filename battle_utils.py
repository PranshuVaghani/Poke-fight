# This file includes the utility function required for fighting.
# Functions include accuracy of a move, effectiveness of a move, dmg done by a move.

import random

# Dictionary containing all the pokemon types and their effectiveness.
TYPE_EFFECTIVENESS = {
    "normal":    {"rock": 0.5, "ghost": 0.0, "steel": 0.5},
    "fire":      {"fire": 0.5, "water": 0.5, "grass": 2.0, "ice": 2.0, "bug": 2.0, "rock": 0.5, "dragon": 0.5, "steel": 2.0},
    "water":     {"fire": 2.0, "water": 0.5, "grass": 0.5, "ground": 2.0, "rock": 2.0, "dragon": 0.5},
    "electric":  {"water": 2.0, "electric": 0.5, "grass": 0.5, "ground": 0.0, "flying": 2.0, "dragon": 0.5},
    "grass":     {"fire": 0.5, "water": 2.0, "grass": 0.5, "poison": 0.5, "ground": 2.0, "flying": 0.5, "bug": 0.5, "rock": 2.0, "dragon": 0.5, "steel": 0.5},
    "ice":       {"fire": 0.5, "water": 0.5, "grass": 2.0, "ice": 0.5, "ground": 2.0, "flying": 2.0, "dragon": 2.0, "steel": 0.5},
    "fighting":  {"normal": 2.0, "ice": 2.0, "rock": 2.0, "dark": 2.0, "steel": 2.0, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "ghost": 0.0, "fairy": 0.5},
    "poison":    {"grass": 2.0, "fairy": 2.0, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0.0},
    "ground":    {"fire": 2.0, "electric": 2.0, "grass": 0.5, "poison": 2.0, "flying": 0.0, "bug": 0.5, "rock": 2.0, "steel": 2.0},
    "flying":    {"electric": 0.5, "grass": 2.0, "fighting": 2.0, "bug": 2.0, "rock": 0.5, "steel": 0.5},
    "psychic":   {"fighting": 2.0, "poison": 2.0, "psychic": 0.5, "dark": 0.0, "steel": 0.5},
    "bug":       {"fire": 0.5, "grass": 2.0, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2.0, "ghost": 0.5, "dark": 2.0, "steel": 0.5, "fairy": 0.5},
    "rock":      {"fire": 2.0, "ice": 2.0, "fighting": 0.5, "ground": 0.5, "flying": 2.0, "bug": 2.0, "steel": 0.5},
    "ghost":     {"normal": 0.0, "psychic": 2.0, "ghost": 2.0, "dark": 0.5},
    "dragon":    {"dragon": 2.0, "steel": 0.5, "fairy": 0.0},
    "dark":      {"fighting": 0.5, "psychic": 2.0, "ghost": 2.0, "dark": 0.5, "fairy": 0.5},
    "steel":     {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2.0, "rock": 2.0, "fairy": 2.0, "steel": 0.5},
    "fairy":     {"fire": 0.5, "fighting": 2.0, "poison": 0.5, "dragon": 2.0, "dark": 2.0, "steel": 0.5}
}


# This function returns the total effectiveness of the move on the target pokemon.
def move_type_effective(move_type: str, target_type1: str, target_type2: str | None) -> float:
    move_type = move_type.lower()
    target_type_1 = target_type1.lower()
    target_type_2 = target_type2.lower() if target_type2 else None

    eff1 = TYPE_EFFECTIVENESS.get(move_type, {}).get(target_type_1, 1.0)
    eff2 = TYPE_EFFECTIVENESS.get(move_type, {}).get(target_type_2, 1.0) if target_type_2 else 1.0

    return eff1 * eff2

# This fuction returns a boolean value that is if the pokemon hit the target.
def move_accuracy(accuracy: int | None) -> bool:
    if accuracy is None:
        return True
    
    rnnum = random.randint(1,100)
    if rnnum <= accuracy:
        return True
    
    return False


# This function returns the damage a move dealt to the target.
def damage_delt( atk: int, opp_defs: int , sp_atk: int, opp_sp_def: int, power: int | None, damage_class: str,
                 move_type: str , target_type1: str, target_type2: str):
    effective = move_type_effective(move_type, target_type1, target_type2)


    if damage_class == "physical":
        if power is None :
            return 0
        damage = (((atk* power) / (50*opp_defs)) + 2) * random.randint(85, 100) * effective / 100

    elif damage_class == "special":
        if power is None:
                return 0
        damage = (((sp_atk* power) / (50*opp_sp_def)) + 2) * random.randint(85, 100) * effective / 100

    elif damage_class == "status":
        return 0
        
    return max(int(damage), 0) 

