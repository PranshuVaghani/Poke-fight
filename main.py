# The main file

from fastapi import FastAPI
from routers import pokemon_select, user, auth, battle
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Pokemon, Move
import pandas as pd

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Load Pokémon from CSV if not already in DB
def load_pokemon_once():
    db: Session = SessionLocal()
    try:
        existing = db.query(Pokemon).first()
        if existing:
            print("⏩ Pokémon already in the database. Skipping load.")
            return

        print("📥 Loading Pokémon into the database...")
        df = pd.read_csv("pokemon.csv")
        df.rename(columns={
            '#': 'id',
            'Name': 'name',
            'Type 1': 'type_1',
            'Type 2': 'type_2',
            'Total': 'total',
            'HP': 'hp',
            'Attack': 'attack',
            'Defense': 'defense',
            'Sp. Atk': 'sp_atk',
            'Sp. Def': 'sp_def',
            'Speed': 'speed',
            'Generation': 'generation',
        }, inplace=True)

        for _, row in df.iterrows():
            existing = db.query(Pokemon).filter_by(id=int(row['id'])).first()
            if existing:
                continue  # Skip duplicate

            pokemon = Pokemon(
                id=int(row['id']),
                name=row['name'],
                type_1=row['type_1'],
                type_2=row['type_2'] if pd.notna(row['type_2']) else None,
                total=int(row['total']),
                hp=int(row['hp']),
                attack=int(row['attack']),
                defense=int(row['defense']),
                sp_atk=int(row['sp_atk']),
                sp_def=int(row['sp_def']),
                speed=int(row['speed']),
                generation=int(row['generation'])
            )
            db.add(pokemon)
            db.commit()

        print("✅ Pokémon loaded successfully.")

    except Exception as e:
        db.rollback()
        print("❌ Error loading Pokémon:", e)

    finally:
        db.close()

def load_moves_once():
    db: Session = SessionLocal()

    try:
        if db.query(Move).first():
            print("⏩ Moves already exist. Skipping move load.")
            return

        print("📥 Loading moves into the database...")
        df = pd.read_csv("moves.csv")

        for _, row in df.iterrows():
            move = Move(
                name=row['name'],
                power=int(row['power']) if pd.notna(row['power']) else None,
                accuracy=int(row['accuracy']) if pd.notna(row['accuracy']) else None,
                type=row['type'],
                damage_class = row['damage_class'],
                description=row['description']
            )
            db.add(move)
            db.commit()
            db.refresh(move)

            if pd.notna(row.get('pokemon_names')):
                pokemon_names = [name.strip() for name in str(row['pokemon_names']).split(',')]
                for pname in pokemon_names:
                    pokemon = db.query(Pokemon).filter(Pokemon.name.ilike(pname)).first()
                    if pokemon and move not in pokemon.moves:
                        pokemon.moves.append(move)

                db.commit()

        print("✅ Moves loaded and linked successfully.")

    except Exception as e:
        db.rollback()
        print("❌ Error loading moves:", e)

    finally:
        db.close()

# Run data loader on startup
load_pokemon_once()
load_moves_once()

# Include route modules
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(pokemon_select.router)
app.include_router(battle.router)