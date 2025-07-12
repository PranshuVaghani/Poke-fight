# This file gets all the moves from pokeapi.
# DEPENDENT ON POKEAPI.

import requests
import csv
import time
from database import SessionLocal
import models

BASE = "https://pokeapi.co/api/v2"
OUTPUT_FILE = "moves.csv"

def fetch_all_pokemon_names():
    db = SessionLocal()
    names = [p.name.lower() for p in db.query(models.Pokemon).all()]
    db.close()
    return names

def fetch_pokemon_moves(poke_name):
    try:
        resp = requests.get(f"{BASE}/pokemon/{poke_name}", timeout=10)
        resp.raise_for_status()
        return [m["move"]["name"] for m in resp.json()["moves"]]
    except Exception as e:
        print(f"❌ Failed to fetch moves for {poke_name}: {e}")
        return []

def fetch_move_detail(move_name):
    try:
        resp = requests.get(f"{BASE}/move/{move_name}", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        descs = data.get("effect_entries", [])
        desc = next((e["effect"] for e in descs if e["language"]["name"] == "en"), "")
        return {
            "name": data["name"],
            "power": data["power"] or "",
            "accuracy": data["accuracy"] or "",
            "type": data["type"]["name"],
            "damage_class": data["damage_class"]["name"],
            "description": desc
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch move: {move_name}: {e}")
        return None

def main():
    poke_names = fetch_all_pokemon_names()
    seen = {}
    rows = []

    for i, name in enumerate(poke_names):
        print(f"🔄 [{i+1}/{len(poke_names)}] Fetching moves for {name}...")
        move_names = fetch_pokemon_moves(name)
        for m in move_names:
            seen.setdefault(m, {"pokemon": set()})
            seen[m]["pokemon"].add(name)
        time.sleep(0.5)

    for i, (mname, info) in enumerate(seen.items()):
        detail = fetch_move_detail(mname)
        if not detail:
            continue
        detail["pokemon_names"] = ",".join(sorted(info["pokemon"]))
        rows.append(detail)
        print(f"✅ [{i+1}/{len(seen)}] Processed move: {mname}")
        time.sleep(0.5)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "power", "accuracy", "type", "damage_class", "description", "pokemon_names"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n🎉 Done. Saved {len(rows)} moves to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
