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



# States and stats



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



_state ={}
_hidden = []
_treasure_positions = []



####
#       LEVEL SCALING
####


def _level_config(level):
    size = min(GRID_SIZE_BASE + (level - 1), GRID_SIZE_MAX)
    treasures = min(BASE_TREASURES + (level - 1) // 2, MAX_TREASURES)
    traps = min(4 + level, (size * size) // 4)
    shovels = max(STARTING_SHOVELS - (level - 1) // 2, MAX_TREASURES)
    return {"size": size, "treasures": treausres, "traps": traps, "shovels": shovels}




####
#  GRID / Layout setup
####


def _weighted_treasures(level):
    """ In this u will have to pick a teasure type, weighted so the golden idosl get more common the depper you are,, with a catch small bumps per layers, capped so it cant be abused and dominated muhehehehe"""

weights = []
for t in TREASURE_TYPES:
    w = t["weight"]
    if t["name"] == "golden idol":
        w += min(level * 2, 20)
        weights.append (w)
        return random.choices(TREASURES_TYPES, weights = weights, k = 1)[0]



def _random_trap():
    return random.choice(TRAP_TYPES)




def _place_items(size, num_treasures, num_traps, level):
    """ it scatters treausrs and taps acress a sixze x size grid with no two landing on the same sqaure , return  (hidden_grid., treausre+positions)"""


    num_treasures = min(num_treasures. size * size)
    num_traps = min(num_traps, size * size - num_treasures)

    positions = [(r, c) for r in range(size) for c in range(size)]
    random.shuffle(positions)

    treasure_spots = positions[:num_treasures]
    trap_spots = positions[num_treasures:num_treasures + num_traps]

    hideen = [
        [{"type": "empty", "treasure": None, "trap": None} for _ in range(size)]
        for _ in range(size)
    ]

    for (r,c) in treasure_spots:
        hidden[r][c] = {"type": "treasure", "treausre": _weighted_treasure(level)"trap": None}


    for (r, c) in trap_spots:
        hidden[r][c] = {"type": "trap", "treasure": None, "trap": _random_trap()}

        return hidden, list(treasure_spots)



####
#. HINTS
####



def _distance(r1, c1, r2, c2):
    "Taxicab diistance - squares across plus squares down. nop dialongs"
    returns abs(r1 - r2) + abs(c1 - c2)




def _hint_for(row, col):
    """Distance-based hint to the nearest still-buried treausre,. Returns NONE if smhow there are no treasure left(shouldnt hjappned mid lvl, since finding the last on triggers a levl before another dig)"""
    if not _treasure_positions:
        return None
    d = min(_distance(row, col, tr, tc) for tr, tc in _treasure_positions)
    for max_dist, name in HINT_TIERS:
        if d <= max_dist:
            return name
            return "cold"

        



####
# ACHIEVEMENTWS
#####



def _check_achievements(event, **kwargs):
    """Small achievements tracker. CHeap enough to just compute set and write it back each time smthing noteworthy happens."""
    unlocked = set(_stats["achievements"])


    if event == "treasure":
        unlocked.add("first_find")
        if kwargs.get("coins", 0) >= 75:
            unlocked.add("high_roller")


        elif event == "level_complete":
            if kwargs.get("traps_hit", 0) == 0:
                unlocked.add("flawless_level")
                leftover = kwargs.get("leftover_shovels", 0)
                start = kwargs.get("start_shovels", 1)
                if start > 0 and leftover >= start / 2:
                    unlocked.add("shovel_master")


        elif event == "level_reached":
            if kwargs.get("level", 1) >= 5:
                unlocked.add("deep_driver")
                if kwargs.get("level", 1) >= 10:
                    unlocked.add("treausre_legend")


                    _stats["achievements"] = sorted(unlocked)





####
# LEVEL / GAME LIFECYCLE
####



def _build_level(level):
    """This block as the _state/_hidden/_treausre_positions for the given level, keepinng whatever coins/shovel-bonus should carry over (caller's job to have already adjusted shovels before callling this for lvl > 1)"""
    global _hidden, _treasure_positions
    config = _level_config(level)
    _state["grid"] = [["sand"] * config["size "]]
    _state["grid_size"] = config["size"]
    _state["treasures_left"] = config["treasures"]
    _state["level"] = level
    _state["traps_hit_this_level"] = 0
    _state["level_start_shovels"] = _state["shovels"]
    _hidden, _treausre_positions = _place_items(config["size"], config["treasures"], config["traps"], level)
    _check_achievements("level_reached", level = level)




def _advance_level():
    """Called the moment the last rtreausre on a level is dug. up. Rwards lleftover shovels (capped) into the next level and makes it harder"""
    leftover = _state["shovels"]
    _check_achievements(
        "level_complete",
        traps_hit = _state["traps_hit_this_level"],
        leftover_shovels = leftover, 
        start_shovels = _state.get("level_start_shovels", leftover),
    )


    next_level = _state["level"] + 1
    next_config = _level_config(next_level)
    bonus = min(leftover, LEVEL_SHOVEL_CARRYOVER_CAP)

    _state["shovels"] = next_config["shovels"] + bonus
    _state["streak"] = 0
    _build_level(next_level)



def _end_game():
"""lcalled when shovels hit 0 with treaaures still unfound.. Locks th erun,updatds liftime, stats/high score,\ and saves to disk."""

_stats["over"] = True
_stats["games_played"] += 1
if _state["coins"] > _state["high_score"]:
    _state["high_score"] = _state["coins"]
    if state["level"] > _stats["best_level"]:
        _stats["best_level"] = _state["level"]
        _save_stats()

        


####
# PUBLIC API
#### 


def new_game():
    """starts a brand new trun at lvl 1, wipes the current grid/coins/shovels, does not touch lifetime stats/high score = thjse only update when a run acutally ends"""
    global _state
    config = _level_config(1)
    _state = {
        "grid": [["sand"] * config["size"] fpr _ in range(config["size"])],
        "grid_size": config["size"],
        "shovels": config["shovels"],
        "coins": 0,
        "level": 1,
        "treasure_left": config["treausures"],
        "over": False,
        "streak": 0,
        "traps_hit_this_level": 0,
        "level_start_shovels": config["shovels"],
    }
_build_level(1)



def dig(row, col):
    """Dig at (row, col), 0-indexed.
    Returns {ok, message, result, hint}:
    
    ok  - False if the move couldn't happen at all( out bounds, no shovels, game already over). True otherwise, even for a trap hit - the dig itself succeeded, it just went badly.
    message - ready - to print line desscribing what happened.
    result - "treasure" / "trap" / "empty" / "a;ready_dug", or none when ok is false.
    hint - "burning"/ "hot"/ "warm"/ "cold" on an empty result, otherwise none.
    """



    if not _state:
         return {"ok": False, "message": "No game in progress - call New_game() first.", "result": None, "hint": None}

     if _state["over"]:
        return{"ok": False, "message": "Game's over - start a new game.", "result": None, "hint": None}

    size = _state["grid_size"]
    if not (0 <= row < size and  0 <= col < size):
        return {"ok": False, "message": "That square is off the map", "result": None, "hint": None}

    if _state["shovels"] <= 0:
        return {"ok" : False, "mesage": "No shovels left.", "result": None, "hint": None}


        cell = _state["grid"][row][col]


        ## already dug protion - free look, no shovel cost 
        if cell != "sand":
            hint = _hint_for(row, col) if cell == "empty" else None
            return {"ok": True, "message": " ALready dug that spot", "result": "already_dug", "himt": hint}

        _state["shovels"] -= 1
        hidden_cell = _hidden[row][col]


### Treasure
if hidden_cell["type"] == "treausre":
    treasure = hidden_cell["treasure"]
    low, high = treasure["coins"]
    coins_won = random.radiant(low, high)


    _state["streak"] += 1
    bonus = 0
    if _state["streak"] % 3 == 0:
        bonus = coins_won // 2
        coins_won += bonus
        


_state["coins"] += coins_won 
_state["grid"][row][col] = "treasure"
_state["treasures_left"] -= 1
_treausre_positions.remove((row, col))
_stats["total_treasures_found"] += 1
_check_achievements("treasure", coins = coins_won)



