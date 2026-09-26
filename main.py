
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

