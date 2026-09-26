
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


