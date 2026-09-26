"""main.py - the terminal front end for the treasure hunt.
 
All the game rules live in hunt.py. This file only draws things,
reads what you type, and passes digs through to hunt.dig().
"""
 
import hunt
 
# the grid grows from 8 up to 14 wide, so we need 14 letters
LETTERS = "ABCDEFGHIJKLMN"
 
 
def symbol_for(cell):
    # "sand" -> "~"  "empty" -> "."  "treasure" -> "$"  "trap" -> "x"
    if cell == "sand":
        return "~"
    elif cell == "empty":
        return "."
    elif cell == "treasure":
        return "$"
    elif cell == "trap":
        return "x"
    return "?"
 
 
def parse_coord(text, size):
    # "D5" -> (4, 3)   row = digit minus one, col = letter's position
    # anything that isn't a square on this grid -> None
    text = text.strip().upper().replace(" ", "")
    if len(text) < 2:
        return None
 
    letter = text[0]
    number = text[1:]
 
    if letter not in LETTERS[:size]:
        return None
    if not number.isdigit():
        return None
 
    row = int(number) - 1
    col = LETTERS.index(letter)
 
    if row < 0 or row >= size:
        return None
    return (row, col)
 
 
def draw_grid(state):
    size = state["grid_size"]
 
    # letter header, lined up with the columns below
    print("    " + " ".join(LETTERS[:size]))
 
    for r in range(size):
        cells = " ".join(symbol_for(cell) for cell in state["grid"][r])
        # row numbers go up to 14, so pad them to 2 characters
        print(f" {r + 1:>2} {cells}")
 
 
def draw_status(state):
    print(
        f"Level {state['level']}  |  "
        f"Shovels: {state['shovels']}  |  "
        f"Coins: {state['coins']}  |  "
        f"Treasures left: {state['treasures_left']}  |  "
        f"Streak: {state['streak']}"
    )
 
 
def show_help(size):
    last = LETTERS[size - 1]
    print()
    print(f"Type a square to dig it, like D5 (columns A-{last}, rows 1-{size}).")
    print("Empty squares tell you how close the nearest treasure is:")
    print("  burning > hot > warm > cold")
    print("Traps cost extra shovels. The explosive mine ends the run.")
    print(f"Other commands:  buy  (1 shovel for {hunt.SHOVEL_COST_IN_COINS} coins)   help   quit")
    print("Map:  ~ sand   . empty   $ treasure   x trap")
    print()
 
 
def choose_difficulty():
    while True:
        choice = input("Difficulty - easy, normal or hard? [normal] ").strip().lower()
        if choice == "":
            choice = "normal"
        if hunt.set_difficulty(choice):
            return choice
        print("Pick one of: easy, normal, hard.")
 
 
def do_dig(state, text):
    spot = parse_coord(text, state["grid_size"])
    if spot is None:
        last = LETTERS[state["grid_size"] - 1]
        print(f"'{text}' isn't a square. Try something like D5 (A-{last}, 1-{state['grid_size']}).")
        return
 
    row, col = spot
    result = hunt.dig(row, col)
    print(result["message"])
 
 
def level_clear_screen(state):
    print()
    print("=" * 40)
    print(f"  LEVEL {state['level'] - 1} CLEARED!")
    print(f"  On to level {state['level']}: {state['grid_size']}x{state['grid_size']} grid,")
    print(f"  {state['treasures_left']} treasures, {state['shovels']} shovels.")
    print("=" * 40)
 
 
def game_over_screen(state, old_high):
    print()
    draw_grid(state)
    print()
    print("=" * 40)
    print("  GAME OVER")
    print(f"  You reached level {state['level']} with {state['coins']} coins.")
    if state["coins"] > old_high:
        print(f"  NEW HIGH SCORE: {hunt.high_score()}!")
    else:
        print(f"  High score: {hunt.high_score()}")
    print("=" * 40)
 
 
def play_one_game():
    choose_difficulty()
    hunt.new_game()
    old_high = hunt.high_score()
    show_help(hunt.get_state()["grid_size"])
 
    while True:
        state = hunt.get_state()
        if state["over"]:
            game_over_screen(state, old_high)
            return
 
        print()
        draw_status(state)
        draw_grid(state)
        text = input("Dig where? ").strip()
        command = text.lower()
 
        if command == "":
            continue
        elif command in ("quit", "q"):
            print("Leaving the beach. Bye!")
            return
        elif command in ("help", "h", "?"):
            show_help(state["grid_size"])
        elif command in ("buy", "b"):
            print(hunt.buy_shovel()["message"])
        else:
            do_dig(state, text)
            if hunt.get_state()["level"] > state["level"]:
                level_clear_screen(hunt.get_state())
 
 
def main():
    print("=" * 40)
    print("  TREASURE HUNT")
    print(f"  High score: {hunt.high_score()}")
    print("=" * 40)
 
    while True:
        play_one_game()
        again = input("\nPlay again? (y/n) ").strip().lower()
        if not again.startswith("y"):
            print("Thanks for playing!")
            break
 
 
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")