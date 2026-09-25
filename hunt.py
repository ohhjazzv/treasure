"""hunt.py

Its a treasure hunt game rules portion

EVERYthing for the Game THE RULES OF GAME lives here. IT doesnt have input(), no drawings so, prints, no input functions etc
This file simply js tracks the states and answer qns abt it thorught the 3 fns:


new_game()
dig(row, col) -> {ok, messagem result, hint}
get_state() -> {grid, shovels, coinsk lvel, trasure_left, over ..}
high_score() -> number





###
ERM GAME DESING NOTES - JAZ


GRID
    the games starts 8*8, grow by 1 per lvel, caps out at GRID_SIZE_MAX so it doesn't get absurd. CELLS are one of:
    "sand" - undug, hides whatever's underneath

    
"""





import json
import os
import random


GRID_SIZE_BASE = 8
GRID_SIZE_MAX = 14
MIN_SHOVELS = 6
BASE_TRASURES = 3
MAX_TREASURES = 6
SHOVEL_COST_IN_COINS = 8
LEVEL_SHOVEL_CARRYOVER_CAP = 3


TRASURES_TYPES = [
    {"name": "common chest", "coins": (10,20), "weight": 60},
    {"name": "rare gem", "coins": (30,50), "weight": 30},
    {"name": "golden idol", "coins": (75,100), "weight":10},
]



TRAP_TYPES = [
    {"name": "pitfall", "cost": 2, "message": "You fall into a pitfall!"},
    {"name": "quicksand", "cost": 3, "message": "Quicksand grabs your shovel!"},
    {"name": "buried spikes", "cost": 2, "message": "Ocuh, Spikes! That hurt"},
]



HINT_TIERS = [
    (1, "burning"),
    (2, "hot"),
    (4, "warm"),
]



SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hunt_save.json")


_DEFAULT_STATS = {
    "high_score": 0,
    "games_played": 0,
    "total_treasures_found": 0,
    "total_traps_hit": 0,
    "best_level": 1,
    "achievements": []
}





def _load_stats():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            merged = dict(_DEFAULT_STATS)
            merged.update(data)
            return merged
    except (FileNotFoundError, json.JSONDecodeError, ValueError, OSError):
        return dict(_DEFAULT_STATS)



def _save_stats():
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(_stats, f)
    except OSError:
        pass


_stats = _load_stats()


