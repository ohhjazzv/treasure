"""hunt.py

Its a treasure hunt game rules portion

EVERYthing for the Game THE RULES OF GAME lives here. IT doesnt have input(), no drawings so, prints, no input functions etc
This file simply js tracks the states and answer qns abt it thorught the 3 fns:


new_game()
dig(row, col) -> {ok, messagem result, hint}
get_state() -> {grid, shovels, coinsk lvel, trasure_left, over ..}
high_score() -> number


row/col passed into dig() are already 0-indexed - main.py tunrs "D5" into (3,4) before calling. Everything about the translaition, drawing the grid, and rejecting junk input is in main not in this file
Bonus stuffs are bolted on beyond the original 4, all optional for main.py to use: 
get_states() -> lifetime stats + unloked achiemvemt
buy_shovel() -> spend coins mid-run for an extra shovel


###
ERM GAME DESING NOTES - JAZ


GRID
    the games starts 8*8, grow by 1 per lvel, caps out at GRID_SIZE_MAX so it doesn't get absurd. CELLS are one of:
    "sand" - undug, hides whatever's underneath
    "empty" - dug, nothing here
    "treasure" - dug, trasure was here
    "trap" - dug, trap went off here

    

TREASURES
    It has 4 teris(common / rare/ golden/ legendary), each with its own coin range. Golden idols get more likely the deeper you ho; the legendary crown does'nt even apperear until lvl 3, then slowly gets more common.

TRAPS
    4 flavors, each costs a different number of shovels, except the expolsive 
    mine, which is rare but ends the run instantly regardless of how many
    shovels you had left. All traps reset your find streak.


DIFFICULTy
    set_difficulty("easy"/ "normal"/ "hard") shifts starting shovels and trap
    density before your new_gae(). Dosent touch anything else abt level scaling.
"""





import json
import os
import random


GRID_SIZE_BASE = 8
GRID_SIZE_MAX = 14
STARTING_SHOVELS = 15
MIN_SHOVELS = 6
BASE_TREASURES = 3
MAX_TREASURES = 6
SHOVEL_COST_IN_COINS = 8
LEVEL_SHOVEL_CARRYOVER_CAP = 3


TREASURES_TYPES = [
    {"name": "common chest", "coins": (10,20), "weight": 55, "min_level": 1},
    {"name": "rare gem", "coins": (30,50), "weight": 28, "min_level": 1},
    {"name": "golden idol", "coins": (75,100), "weight":12, "min_level": 1},
    {"name": "legendary crown", "coins": (150,200), "weight": 5, "min_level": 3},
]



TRAP_TYPES = [
    {"name": "pitfall", "cost":2, "weight": 40, "message": "You fall into a pitfall!"},
    {"name": "quicksand", "cost": 3, "weight": 25, "message": "Quicksand grabs your shovel!"},
    {"name": "buried spikes", "cost": 2, "weight": 25, "message": "Ouch spikes! That hurt."},
    {"name": "explosive mine", "cost": 0, "weight": 10, "instant": True, "message": "BOOOOOM! THE mine goes off!!!"},
]


DIFFICULTY_PRESETS = {
    "easy": {"shovel_bonus": 5, "trap_multiplier": 0.6},
    "normal": {"shovel_bonus": 0, "trap_multiplier": 1.0},
    "hard": {"shovel_bonus": -4, "trap_multiplier": 1.5},
}



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
        "total_shovels_used": 0,
        "best_level": 1,
        "achievements": [],
        "leaderboard": [],
}

_MAX_LEADERBOARD_ENTIRES = 5

_difficulty = "normal"

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
    preset = DIFFICULTY_PRESETS.get(_difficulty, DIFFICULTY_PRESETS["normal"])
    size = min(GRID_SIZE_BASE + (level - 1), GRID_SIZE_MAX)
    treasures = min(BASE_TREASURES + (level - 1) // 2, MAX_TREASURES)
    traps = min(4 + level, (size * size) // 4)
    shovels = max(STARTING_SHOVELS - (level - 1) // 2, MAX_TREASURES)
    return {"size": size, "treasures": treasures, "traps": traps, "shovels": shovels}




####
#  GRID / Layout setup
####


def _weighted_treasures(level):
    """ In this u will have to pick a teasure type, weighted so the golden idosl get more common the depper you are,, with a catch small bumps per layers, capped so it cant be abused and dominated muhehehehe"""
avialable = [t for t in TREASURES_TYPES if level >= t.get("min_level", 1)]
weights = []
for t in avialable:
    w = t["weight"]
    if t["name"] == "golden idol":
        w += min(level * 2, 20)
        if t["name"] == "legendary crown":
            w += min((level - t["min_level"]) * 2, 15)
        weights.append (w)
        return random.choices(avialable, weights = weights, k = 1)[0]



def _weighted_trap(level):
    """PICk a trap type, weight so the instant expolsive mine statys rare but creeps bup as lvl goes on """
    weights = []
    for t in TRAP_TYPES:
        w = t["weight"]
        if t.get("instant"):
            w += min(level, 8)
            weights.append(w)
            return random.choices(TRAP_TYPES, weights= weights, k = 1)[0]



def _place_items(size, num_treasures, num_traps, level):
    "SScatter treausre and traps across a ssize x size grid with no two landing on the same square. Returns (hiddne_grid, Trasures_positionss)."
    num_treasures = min(num_treasures, size * size)
    num_traps = min(num_traps, size * size - num_treasures)

    positions = [(r,c) for r in range(size) for c in range(size)]
    random.shuffle(positions)

    treasures_spots = positions[:num_treasures]
    trap_spots = positions[num_treasures:num_treasures + num_traps]

    hidden  = [
        [{"type": "empty", "treasure": None, "trap": None} for _ in range(size)]
        for _ in range(size)
    ]

    for (r, c) in treasure_spots:
        hidden[r][c] = {"type": "treasure", "treasure": _weighted_treasures(level), "trap": None}
        for (r,c) in trap_spots:
            hidden[r][c] = {"type": "trap", "treasure": None, "trap": _weighted_trap(level)}


            return hidden, list(treasures_spots)
    

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




def _update_leaderboard():
    """Drop this run's result into the leaderbord, keep it sorted by coins descending and trim it back down to top N"""
    board = _stats.get("leaderboard", [])
    board.append({"coins": _state["coins"], "level": _state["level"]})
    board.sort(key=lambda entry: entry["coins"], reverse = TRUE)
    _stats["leaderboard"] = board[:_MAX_LEADERBOARD_ENTRIES]



def _end_game():
"""lcalled when shovels hit 0 with treaaures still unfound.. Locks th erun,updatds liftime, stats/high score,\ and saves to disk."""

_stats["over"] = True
_stats["games_played"] += 1
if _state["coins"] > _state["high_score"]:
    _state["high_score"] = _state["coins"]
    if state["level"] > _stats["best_level"]:
        _stats["best_level"] = _state["level"]
        _update_leaderboard()
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
        _stats["total_shovels_used"] += 1
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


message = f"Ypu dug up a {treasure['name']} worth {coins_won} coins!"
if bonus:
    message += f"Streak bonus + {bonus}!"


    if _state["treasures_left"] == 0:
        cleared_level = _state["level"]
        message += f" Level {cleared_level} clear!"
        _advance_level()

        return {"OK": True, "message": message, "result": "treasure", "hint": None}



### Trap

if hidden_cell["type"] == "trap":
trap = hidden_cell["trap"]
cost = trap [ "cost"]
_state["shovels"] = max(0, _state["shovels"] - cost)
_state["streak"] = 0
_state["traps_hit_this_level"] += 1
_state["grid"][row][col] = "trap"
_stats["total_traps_hit"] += 1


if trap.get("instant"):
    message = f"{trap['message']} Run Over instantly"
    _end_game()
    return {"ok": True, "message": message, "result":"trap", "hint": None}

cost = trap["cost"]
_state["shovels"] = max(0, _state["shovels"] - cost)
message = f"{trap['message']} lost {cost} extra shovels."


if _state["shovels"] <= 0 and _state["treasures_left"] > 0:
    _end_game()
    message += " OUT of thsovel = game over"

    return {"ok": True, "message": message, "result": "trap", "hint": None}


### empty


_state["grid"][row][col] = "empty"
_state["Streak"] = 0
hint = _hint_for(row, col)
message = f"NTH here. Feels{hint}."



if _state["shovels"] <= 0 and _state["treasures_left"]  >  0:
    _end_game()
    message += " OUT OF SHOVEELS _ GAME OVER"

    return {"ok": True, "message": message, "result": "empty", "hint": hint}




def get_state():
    """Snapshot of the current run ; Grid is copied.  sthe caller cant accidentally mutate interal state by poking at the reutned list"""
    if not _state:
        return {
            "grid": [], "shovels": 0, "coins": 0, "level": 0, "treasures_left": 0, "over": True, "grid_size": 0, "streak": 0,
        } 

    return {
        "grid": [row[:] for row in _state["grid"]],
        "shovels": _state["shovels"],
        "coins": _state["coins"],
        "level": _state["level"],
        "treasires_left": _state["treasures_left"],
        "over": _state["over"],
        "grid_size": _state["grid_size"],
        "streak": _state["streak"],
    }



def high_score():
    """Best coin total ever reached across all runs,. loaded from disk."""
    return _stats["high_score"]




###
# BONUS EXTRAS
####]



def get_stats():
    """Lifetime stats and unlocked achievements, independent of current run."""
    return {
        "high_score": _stats["high_score"],
        "games_played": _stats["games_played"],
        "total_treasures_found": _stats["total_treasures_found"],
        "total_traps_hit": _stats["total_traps_hit"],
        "total_shovels_used": _stats["total_shovels_used"],
        "best_level": _stats["best_level"],
        "achievements": list(_stats["achievements"]),
    }



def set_difficulty(name):
    """Switch difficulty preset ("easy" / "normal" / "hard"). Takes effect on the next new_game() - doesn't touch a run already in progress. 
    rREturns true if it was real preset name., false otherwise"""
    global _difficulty
    if name not in DIFFICULTY_PRESETS:
        return False
    _difficulty = name
    return True



def get_difficulty():
    """Currently acgtive difficulty preset name."""
    return _difficulty



def get_leaderboard():
    """Tops runs ever, sorted best-frist each as {"coins": int, "level": int}.
    capped at _MAX_LEADERBOARD_ENTREIS entreis."""
    return [dict(entry) for entry in _stats.get("leaderboard", [])]



def reset_stats():
    """Wipe all lifetime stats/achievements/leaderboard/high score back to tdefaults and save that over whatever was on dislk. Doesn''t touch the current in-progress run. Useful for "rest high score" mewnu options"""
    global _stats
    _stats = dict(_DEFAULT_STATS)
    _stats["achievements"] = []
    _stats["leaderboard"] = []
    _save_stats()
    return True



def get_legend():
    """Static reference info abt treasures/ traps/ hints, handy for 'how to play' screen. Doesn't reveal anythhing about the current grid just the general rules, same for every run."""
    return {
        "treasures": [
            {"name": t["name"], "coins": t["coins"], "min_level": t.get("min_level", 1)}
            for t in TREASURES_TYPES
        ],

        "traps": [
            {"name": t["name"], "cost": t.get("cost", 0), "instant": t.get("instant", False)}
            for t in TRAP_TYPES
        ],

        "hints": [{"max_distance": d, "name": name} for d, name in HINT_TIERS] + [{"max_distance": None, "name": "cold"}],
        
        "difficulties": list(DIFFICULTY_PRESETS.keys()),
    }


def buy_shovel():
    """Spends SHOVEL_COST_IN_COINS coins for one extra shovel min-run. 
    Returns {ok, message}. Purely optional - main.py doesnt have to expose this at all"""
    if not _state or _state["over"]:
        return {"ok": False, "message": "No active game to buy a shovel for."}
    if _state["coins"] < SHOVEL_COST_IN_COINS:
        return {"ok": False, "message": f"Need {SHOVEL_COST_IN_COINS} coins, you've got {_state['coins']}."}
    _state["coins"] -= SHOVEL_COST_IN_COINS
    _state["shovels"] += 1
    return {"ok": True, "message": f"bought a shovel for { SHOVEL_COST_IN_COINS} coins."}


new_game()


