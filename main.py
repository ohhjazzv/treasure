
import os
import random
import string
import sys
import time
import hunt 



##################################
## TERMINAL / COLOR SETUP
#################################

if os.name == "nt":
    os.system("")



    USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
    ANIMATORS_ENABLED =  True
    GAME_VERSION = "1.0"



    def toggle_color():
        global USE_COLOR
        USE_COLOR = not USE_COLOR
        return USE_COLOR



    def toggle_animatinos():
        global ANIMATIONS_ENABLED
        ANIMATIONS_ENABLED = not ANIMATIONS_ENABLED
        return ANIMATIONS_ENABLED



class C:
    """ANSI color/style codes!!! TOOK ME A HELLL LNOG FIGURING TS OPUT UGH"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GREY = "\033[90m"



def colorize(text, color_code):
    """It warps the text in a color codes, uncless color's disbabled - then js hand back the plain text untouched"""
    if not USE_COLOR or not color_code:
        return text
        return f"{color_code}{text}{C.RESET}"
    


CELL_SYMBOLS = {
    "sand": "~",
    "empty": ".",
    "treasure": "$",
    "trap": "X",
}


CELL_COLORS = {
    "sand": C.YELLOW + C.DIM,
    "empty": C.GREY,
    "treasure": C.YELLOW,
    "trap": C.RED + C.BOLD,
}


HINT_COLORS = {
    "burning": C.RED + C.BOLD,
    "hot": C.MAGENTA,
    "warm": C.YELLOW,
    "cold": C.CYAN,
}


RESULT_COLORS = {
    "treasure": C.YELLOW + C.BOLD,
    "trap": C.RED + C.BOLD,
    "empty": C.WHITE,
    "already_dug": C.GREY,
    None: C.RED,
}






##############################################################
## FLAVOUR TEXT
##############################################################

## SM FUNNYY BONUS STUFF


FLAVOR_TREASURE = [
    "The sand practically glitters where you found it",
    " YOur pockets are heavier ad your shovel arm is tired. Fair trade",
    "smwhere, a crab is jealous of you rgood fortune",
    "yoy do small, dignified victory shuffle",
]


FLAVOUR_TRAP = [
    "Not to self: check twice, dig once MUEHEHHE!",
    "the sand really didnt want to be disturbed there",
    "THAT one's going in the highligght reel. THE BAD KINDA",
    "You mutter smthing not fit for print",
]


FLAVOR_EMPTY = [
    "JUST sand. LOST and lots of sand",
    "BNTH but a very unimpressed crab",
    "you've briefly become obn with disspointed",
    "the hole staes back at you, equally empty",
]


TIPS = [
    "Traps reset your streak, so don't get greedy chasing a bonus",
    "The legendary crown never shows up before lvl 3. Patience",
    "Expolosive mines get slightly more commmon the deeper you go",
    "Already-diug squares are free to re check no shovel costs",
    "Buying a shovel spends coins you could've kept . ONlyt worht it in a pinch",
    "Hints only ever point at the neartest treasure,. not all of them,",
    "a flawless lvl (no traps hit) is its own achievements",
]


ACHIEVEMENTS_INFO = {
    "first_find": ("Fiirst Find", "DUg up your very first treausre"),
    "high_roller": ("High Roller", " Found a treasure wrroth 75+ coins in one dig"),
    "flawless_level": ("Flawless", "Cleared a lvl without hitting  a single trap."),
    "shovel_master": ("Shovel Master", "Cleared a lvl with at laeast half your shovels left."),
    "deep_driver": ("DEEP Driver", "Reaeched lvl 5."),
    "treasure_legend": ("Treasure Legned", "Reached lvl 10."),
}




##################################################################
## SAMLL UTILITIES
##################################################################



def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")



def safe_input(prompt=""):
    try:
        return input(prompt)
    except(EOFError, KeyboardInterrupt):
        print()
        print("Thanks for playing - see u next dig")
        sys.exit(0)



def wait_for_enter(message="Press ENTER to continue....", short = False):
    if short:
        message = "PRESS ENTER"
        sage_input(colorize(message, C.GREY))



def confirm(prompt):
    "YES/nop prompt. Anything starting with 'y' counts as yes, everything else (including js hutting enter) counts as no."
    answer = safe_input(prompt).strip().lower()
    return answer.startswith("y")



def suspense():
    "Tiny pausw with dots before reavling a dig result. Purely for feel - slkippied if animations are turned off in settings, or if there's no real termnial to animatre in anyway"

    if not ANIMATINOS_ENABLED or not USE_COLOR:
        return 
    sys.stdout.write("Digging")
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(0.12)
        sys.stdout.write(".")
        sys.stdout.flush()
        print()



def pluralize(count, singular, plural=None):
    if plural  is None:
        plural = singular + "s"
        return f"{count} {singular if count == 1 else plural}"



def format_table(headers, rows):
    "Simple aligned text table"
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, call in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))



def fmt_row(cells):
    return "". join(str(c).ljust(widths[i]) for i, c in enumerate(cells))
lines = [fmt_row(headers), fmt_row(["-" * w for w in widths])]
for row in rows:
    lines.append(fmt_row(row))
    return "\n".join(lines)






########################################################
### BANNERS
########################################################




def big_banner():
    line = "=" * 52
    title = "X MARKS THE SPOT - TREASURE HUNT X"
    chest = [
            r"         --------------------------------------------",
            r"        /     .-'''''''''''''''''''''''''''-.        \\",
            r"       /     /    $.    $.     $.     $.      \        \\",
            r"      |      | ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  |        |",
            r"      |      | _______________________________|        |",
            r"       \_______________________________________________/",
    ]

    parts = [colorize(line, C.YELLOW)]
    parts.append(colorize(title.center(52), C.YELLOW + C.BOLD))
    parts.append(colorize(line, C.YELLOW))

    for row in chest:
        parts.append(colorize(row, C.YELLOW + C.DIM))
        return "\n".join(parts)



def banner_small():
    line = "=" * 40
    return colorize(line, C.GREY) + "\n" + colorize("TREASURE HUNT".center(40), C.YELLOW + C.BOLD) + "\n" + colorize(line, C.GREY)



def random_tip():
    return colorize("Tip: ", C.CYAN + C.BOLD) + random.choice(TIPS)




############################################################################
### INPUT PARSING
############################################################################



def parse_coordinate(raw, grid_size):
    text = raw.strip()

    if not text:
        return None, None, "Type a square like D5, or a command."


        letter = text[0]
        rest = text[1:].strip()


        if not letter.isalpha():
            return None, None, f"'{text}' doesn't start with a column letter. Try smthing like D5"


        if not rest:
            return None, None, f"'{text}' is missing the row number. Try smthing like {letter.upper()}5."


        if not rest.isdigit():
            return None, None, f"'{rest}' isn't a row number. Try smthing like {letter.upper()}5"


            letter = letter.upper()
            number = int(rest)


            valid_letters = string.ascii_uppercase[:grid_size]
            if letter not in valid_letters:
                return None, None, f"Column '{letter}' is off the grid. Use A-{valid_letters[-1]}."


            if not (1 <= number <= grid_size):
                return None, None, f"Row '{number} is off the grid. use 1-{grid_size}."


                row = number - 1          
                col = valid_letters.index(letter)
                return row, col, None




#######################################################################
## GRID/STATUS RENDERING
######################################################################



def render_grid(state):
    size = state["grid_size"]
    letters = string.ascii_uppercase[:size]
    row_label_width = len(str(size))


    header = "" * (row_label_width + 2) + "".join(f"{l:>2}" for l in letters)
    divider = "" * (row_label_width + 1) + "+" + "+".join(["---"] * size) + "+"


    lines = [header, divider]
    for r in range(size):
        cells = []
        for c in range(size):
            cell_type = state["grid"][r][c]
            symbol = CELL_SYMBOLS.get(cell_type, "?")
            color = CELL_COLORS.get(cell_type, "")
            cells.append(colorize(f" {symbol}", color))
            row_label = str(r + 1).rjust(row_label_width)
            lines.append(f"{row_label} |" + "|".join(cells) + "|")
            lines.append(divider)

        return "\n".join(lines)

    

def render_status(state):
    parts = [
        f" Level {state['level']}",
        f"{colorize('Shovels', C.CYAN)}; {state['shovels']}",
        f"{colorize('Coins', C.YELLOW)}: {state['coins']}",
        f"Treasures left: {state['treasures_left']}",
    ]

    if state.get("Streak", 0) >= 2
    parts.append(colorize(f"Streak x{state['streak']}", C.MAGENTA + C.BOLD))
    return "".join(parts)



def rander_legend_line():
    bits = [
        colorize("~", CELL_COLORS["sand"]) + "sand",
        colorize(".", CELL_COLORS["empty"]) + "empty",
        colorize("S", CELL_COLORS["treasure"]) + "treasure",
        colorize("X", CELL_COLORS["trap"]) + "trap",
    ]

    return "".join(bits)



###############################################
#### DIG. RESULT DISPLAY
###############################################



def display_dig_result(result):
    color = RESULT_COLORS.get(result["result"], C.WHITE)
    print(colorize(result["message"], color))


if result.get("hint"):
    hint_color = HINT_COLORS.get(result["hint"], C.WHITE)
    print(f"Feeling: {colorize(result['hint'].upper(), hint_color)}")


    flavor_pool = {
        "treasure": FLAVOR_TREASURE,
        "trap": FLAVOR_TRAP,
        "empty": FLAVOR_EMPTY,
    }.get(result["result"])

    if flavor_pool:
        print(colorize("" + random.choice(flavor_pool), C.GREY))



def show_level_up(new_level):
    print()
    message = f"*** :EVE: {new_level}! THe grid grows, the sand shifts ... ***"
    print(colorize(message, C.GREEN + C.BOLD))

    if USE_COLOR:
        time.sleep(0.6)




#######################################################
### HOW TO PLAY/ LEARDERBOARD/ STATS/ DIFFICTULY
########################################################



def show_legend():
    legend = hunt.get_legend()
    clear_screen()
    print(colorize("HOW TO PLAY", C.YELLOW + C.BOLD))
    print(colorize("=" * 44, C.YELLOW))
    print() 
    print("DIG a sqaure by typing its column letter and row number, like D5")
    print("Each real dif costs 1 shovel - akready-dug squares are free to")
    print("re-check. Find every treasure to clear the level; the grid grows")
    print("and shovels get scarcer the further you go.")
    print()


    print(colorize("Treasures", C.YELLOW + C.BOLD))
    rows = []

    for t in legend["treasures"]:
        coin_range = f"{t['coins'][0]}-{t['coins'][1]}"
        unlocks = "From the start" if t["min_level"] <= 1 else f"Level {t['min_level']}+"
        rows.append([t["name"].title(), coin_range, unlocks])
    print(format_table(["Treasure", "Coins", "Unlocks"], rows))
    print()

    print(colorize("Traps", C.RED + C.BOLD))
    rows = []

    for t in legend["traps"]:
        effect = "Ends the run intstantly!" if t["instant"] else f"-{t['cost']} shovels"
        rows.append([t["name"].title(), effect])

    print(format_table(["Trap", "Effect"], rows))
    print()

    print(colorize("Hints", C.MAGENTA + C.BOLD))
    rows = []
    prev = 0


    for h in legend["hints"]:
        if h["max_distance"] is None:
            distance = f"{prev + 1}+ sqaures"

        elif h["max_distance"] == prev + 1:
            distance = f"{h['max_distance']} sqaure" if h["max_distance"] == 1 else f"{h['max_distance']} sqaures"

        else:
            distance = f"{prev + 1}-{h['max_distance']} squares"

        rows.append([h["name"].title(), distance])

        if h["max_distance"] is not None:
            prev = h["max_distance"]


    print(format_table(["Feeling", "Distance to nearest treasure"], rows))
    print()

    print(colorize("Streaks, SHhovels & Diffiulty", C.CYAN + C.BOLD))
    print("- EVERy 3rd treasure found in a row ( no trap in between) pays +50%")
    print(f"- Buy an extra shovel mid-run for {hunt.SHOVEL_COST_IN_COINS}coins with the BUY command.")
    print(f"- Difficulties avaiable: {','.join(d.title() for d in legend['difficulties'])}.")
    print()

    wait_for_enter()



def show_leaderboard():
    clear_screen()
    print(colorize("LEADERBOARD", C.YELLOW + C.BOLD))
    print(colorize("=" * 44, C.YELLOW))
    print()

    board = hunt.get_leaderboard()


    if not board:
        print("No runs recorded yet. Go burty some shovels in the sand")
    else:
        rows = [[i + 1, entry["coins"], entry["level"]] for i, entry in enumerate(board)]
        print(format_table(["Rank", "Coins", "Level Reached"], rows))
    print()
    wait_for_enter()



def show_stats():
    clear_screen()
    print(colorize("Your STATS", C.YELLOW + C.BOLD))
    print(colorize("=" * 44, C.YELLOW))
    print()

    stats = hunt.get_stats()
    row = [
        ["High Score", stats["high_score"]],
        ["Games Played", stats["games_played"]],
        ["Treasures Found", stats["total_treasures_found"]],
        ["Traps Hit", stats["total_traps_hit"]],
        ["Shovels Used", stats["total_shovels_used"]],
        ["Best Level Reached", stats["best_level"]],
    ]


    print(format_table(["Stat", "Value"], rows))
    print()

    print(colorize("Achievements", C.CYAN + C.BOLD))
    unlocked = set(stats["Achievements"])

    for key, (title, desc) in ACHIEVEMENTS_INFO.items():
        if key in unlocked:
            print(colorize(f" [x] {title}", C.GREEN + C.BOLD) + f" - {desc}")
        else:
            print(colorize(" [] ???", C.GREY) + "- KEEP playin to unlock")

        print()
        wait_for_enter()



def difficulty_menu():
    mapping = {"1": "easy", "2":"normal", "3":"hard"}
    while True:

        clear_screen()
        print(colorize("DIFFICULTY", C.YELLOW + C.BOLD))
        print(colorize("=" * 44, C.YELLOW))
        print()

        current = hunt.get_difficulty()

        print(f"Current difficulty: {colorize(current.title(), C.CYAN + C.BOLD)}")
        print("(takes effect on your next New Game, won't change a run in progress)")
        print()

        print("1) Easy  - more shovels, fewer traps")
        print("2) Normal - balanced")
        print("3) Hard - fewer shovels, more traps")
        print("B) Back")
        print()

        choice = safe_input("Choose: ").strip().upper()

        if choice in mapping:
            hunt.set_difficulty(mapping[choice])
            print(f"Difficulty set to {mapping[choice].title()}.")
            wait_for_enter(short=True)

        elif choice == "B":
            return

        else:
            print(colorize("Not a valid option.", C.RED))
            wait_for_enter(short=True)



def reset_stats_flow():
    clear_screen()
    print(colorize("RESET STATS", C.RED + C.BOLD))
    print(colorize("=" * 44, C.RED))
    print()


    print("This wipes your high score, leaderbord, lifetime stats, and")
    print("Achievements. It doesnt NOT affect a run currently in profress.")
    print()


    if confirm(colorize("Readyy wipe everything? (Y/N):", C.RED)):
        hunt.reset_stats()
        print(colorize("Done. Clean slate", C.GREEN))
    else:
        print("Cancelled - nth was touched.")
        wait_for_enter()



def settings_menu():
    while True:
        clear_screen()
        print(colorize("SETTINGS", C.YELLOW + C.BOLD))
        print(colorize("=" * 44, C.YELLOW))
        print()

        print(f"1) Color output: {'ON' if USE_COLOR else 'OFF'}")
        print(f"2) Dig animation: {'ON' if ANIMATIONS_ENABLED else 'OFF'}")
        print("B) Back")
        print()

        choice = safe_input("Choose: ").strip().upper()

        if choice == "1":
            toggle_color()
        elif choice == "2":
            toggle_animations()
        elif choice == "B":
            return 
        else:
            print(colorize("Not a valid options", C.RED))
            wait_for_enter(short=True)



def show_about():
    clear_screen()
    print(colorize("About", C.YELLOW + C.BOLD))
    print(colorize("=" * 44, C.YELLOW))
    print()

    print(f"Treasure Hunt v{GAME_VERSION}")
    print("A grid-digging, shovel-counting, and sand-flavoured little game.")
    print()

    print("Rules engine (grid, treasures, traps, saves): hunt.py")
    print("Screen, input prasingm and menus(this file): main.py")
    print()

    print("hunt.py never prints anything and main.py never touches game")
    print("state directly- they only talk throught hunt.py's 4 functions")
    print('(plus a handful of options bonus ones)')
    print()

    wait_for_enter()


    