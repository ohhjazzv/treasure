treasure

a treasure hunt game in your terminal. week 2 of hack club third space, theme was TREASURE.

treasure is buried under a grid of sand. you get limited shovels. type a coordinate like D5 to dig it.

nothing there? it tells you how close you were. burning, hot, warm, cold.

clear a level and you go deeper. bigger grid, more traps, fewer shovels.

some squares have traps. one of them just ends your run on the spot.

grid starts 8x8, goes up to 14x14. four kinds of treasure, the good ones get likelier the deeper you go. the legendary crown doesn't exist until level 3. coins carry over. high score saves to disk.

<<<<<<< HEAD
running it

no dependencies, just python.

python main.py     terminal
python play.py     krish's terminal version, colours and menus
python gui.py      window version, click to dig

three front ends off one rules file.

files

hunt.py — krish. all the game logic, no printing, no input.

main.py — me. terminal front end.

play.py — krish. his terminal front end.

gui.py — tkinter window version.

the contract between them:

new_game()
dig(row, col)  -> {ok, message, result, hint}
get_state()    -> grid, shovels, coins, level, treasures_left, over
high_score()   -> number

dig() takes 0-indexed numbers, so turning D5 into (4, 3) is the front end's job.

in there

4 treasure tiers. 4 trap types, one instant game over. streak bonus every 3 finds. 7 achievements. difficulty presets. top 5 leaderboard. shovel shop, 8 coins each.
=======
## running it

no dependencies, just python.
>>>>>>> 3dcfc70d56e133314ea0d339675dea82da4a3526
