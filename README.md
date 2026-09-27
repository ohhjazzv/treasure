# treasure

a treasure hunt game in your terminal. week 2 of hack club third space, theme was TREASURE.

treasure is buried under a grid of sand. you get limited shovels. type a coordinate like `D5` to dig it.

nothing there? it tells you how close you were. burning, hot, warm, cold.

clear a level and you go deeper. bigger grid, more traps, fewer shovels.

some squares have traps. one of them just ends your run on the spot.

grid starts 8x8, goes up to 14x14. four kinds of treasure, the good ones get likelier the deeper you go. the legendary crown doesn't exist until level 3. coins carry over. high score saves to disk.

## running it

```
python main.py
```

no dependencies, just python.

```
python play.py
```

same game, krish's front end. colour codes, different layout. we both built one so we kept both.

## the split

one rule: the rules file never prints, the front end never decides.

`hunt.py` — krish. all the logic. grid, digging, hints, traps, levels, achievements, saving. zero `print()`, zero `input()`.

`main.py` — me. drawing the grid, parsing `D5`, catching bad input, menus, end screens.

`play.py` — krish's front end.

four functions in between:

```
new_game()
dig(row, col)  -> {ok, message, result, hint}
get_state()    -> grid, shovels, coins, level, treasures_left, over
high_score()   -> number
```

`dig()` takes 0-indexed numbers. turning `D5` into `(4, 3)` is my job. `hunt.py` never sees a letter.

extra stuff on top: difficulty presets, a shop, stats, achievements, a leaderboard. all optional.

## why

last week our farming game didn't fit together until 4am the night before it was due. we'd never agreed what anything was called.

so this time we wrote the contract first. i built against a fake `hunt.py` full of stubs, so neither of us waited on the other.

branches and pull requests too, instead of both pushing to main.

## in there

4 treasure tiers. 4 trap types, one instant game over. streak bonus every 3 finds. 7 achievements. difficulty presets. top 5 leaderboard. shovel shop, 8 coins each.

## known

save file is plain json next to the script. you can just edit your high score. we know.