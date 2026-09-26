# Treasure Hunt

A treasure hunt game, built for Hack Club Third Space, week 2 (theme: **TREASURE**).

Dig squares on a grid of sand. Empty squares tell you how close the nearest treasure is (burning / hot / warm / cold). Traps cost you shovels, and the explosive mine ends the run. Find every treasure to go to the next level: the grid grows from 8x8 up to 14x14. High score and stats are saved between runs.

## Run it

- `python main.py` - terminal version
- `python play.py` - terminal version with menus, colours, stats
- `python gui.py` - window version, click to dig

Needs Python 3.8+, nothing to install.

## Who built what

| File | Built by | What it does |
|---|---|---|
| `hunt.py` | Krish | All the game rules. No printing, no input. |
| `main.py` | Jaz | Terminal front end. |
| `play.py` | Krish | Krish's terminal front end with menus. |
| `gui.py` | Jaz | Tkinter window front end. |

Bug-fixing, parts of `main.py` and `play.py`, and `gui.py` were done with help from Claude (AI).
