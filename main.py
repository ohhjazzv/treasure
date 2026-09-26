

import fakehunt as hunt

LETTERS = "ABCDEFGH"


def symbol_for(cell):
    # None -> "."  treasure -> "$"  trap -> "x"
    # hot -> "h"  warm -> "w"  cold -> "c"
    pass


def draw_grid(state):
    # print the letter header, then each row with its number
    # grid[r][c] is row r, square c
    pass


def parse_coord(text):
    # "D5" -> (4, 5)   bad input -> None
    # .upper(), check length, LETTERS.index(), .isdigit(), range check
    pass


def do_dig(state):
    # ask for a square, parse it, bail if None
    # hunt.dig(row, col), print result["message"]
    pass


while True:
    state = hunt.get_state()
    # header: level, shovels, coins, treasures left
    # draw_grid(state)
    # menu, input, if-chain
    pass

