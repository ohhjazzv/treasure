"""gui.py - a clickable window front end for the treasure hunt.

Same idea as main.py and play.py: every rule lives in hunt.py, and this
file only draws the board and passes clicks through to hunt.dig().
Uses tkinter, which comes with Python, so there's nothing to install.

    python3 gui.py
"""

import tkinter as tk
from tkinter import messagebox

import hunt

LETTERS = "ABCDEFGHIJKLMN"

# ---- colours ------------------------------------------------------------

BG = "#f6ecd4"          # window background, pale sand
PANEL = "#eadcb8"       # status bar / footer
INK = "#3b2f1e"         # main text colour
MUTED = "#8a7858"       # secondary text

SAND = "#dcc07e"        # undug square
SAND_HOVER = "#ecd49a"
EMPTY = "#c9b88f"       # dug, nothing there (before we know a hint)
TREASURE = "#ffc933"
TRAP = "#2f2a26"

HINT_COLORS = {
    "burning": "#e03131",
    "hot": "#f76707",
    "warm": "#ffc078",
    "cold": "#a5d8ff",
}

RESULT_COLORS = {
    "treasure": "#a36a00",
    "trap": "#c92a2a",
    "empty": INK,
    "already_dug": MUTED,
    None: "#c92a2a",
}

ACHIEVEMENT_NAMES = {
    "first_find": ("First Find", "Dug up your first treasure"),
    "high_roller": ("High Roller", "Found 75+ coins in one dig"),
    "flawless_level": ("Flawless", "Cleared a level without hitting a trap"),
    "shovel_master": ("Shovel Master", "Cleared a level with half your shovels left"),
    "deep_driver": ("Deep Diver", "Reached level 5"),
    "treasure_legend": ("Treasure Legend", "Reached level 10"),
}

FONT = "Helvetica"


class TreasureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Treasure Hunt")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.cells = {}          # (row, col) -> Label
        self.hints = {}          # (row, col) -> "hot" etc, for dug empty squares
        self.drawn_size = 0
        self.old_high = 0

        self.build_layout()
        self.new_game()

        root.bind("<n>", lambda e: self.new_game())
        root.bind("<b>", lambda e: self.buy_shovel())

    # ---- layout ---------------------------------------------------------

    def build_layout(self):
        tk.Label(
            self.root, text="X MARKS THE SPOT", bg=BG, fg=INK,
            font=(FONT, 22, "bold"),
        ).pack(pady=(14, 0))
        tk.Label(
            self.root, text="click the sand to dig - hints tell you how close the nearest treasure is",
            bg=BG, fg=MUTED, font=(FONT, 11),
        ).pack(pady=(0, 10))

        # status bar
        bar = tk.Frame(self.root, bg=PANEL, padx=10, pady=6)
        bar.pack(fill="x", padx=16)
        self.stat_labels = {}
        for key, title in [("level", "Level"), ("shovels", "Shovels"), ("coins", "Coins"),
                           ("treasures_left", "Treasures left"), ("streak", "Streak"),
                           ("high", "High score")]:
            box = tk.Frame(bar, bg=PANEL, padx=8)
            box.pack(side="left", expand=True)
            tk.Label(box, text=title, bg=PANEL, fg=MUTED, font=(FONT, 10)).pack()
            value = tk.Label(box, text="-", bg=PANEL, fg=INK, font=(FONT, 16, "bold"))
            value.pack()
            self.stat_labels[key] = value

        # the board gets rebuilt whenever the grid size changes
        self.board = tk.Frame(self.root, bg=BG, pady=12)
        self.board.pack()

        # what just happened
        self.message = tk.Label(self.root, text="", bg=BG, fg=INK,
                                font=(FONT, 14, "bold"), wraplength=560)
        self.message.pack(padx=16)
        self.hover = tk.Label(self.root, text=" ", bg=BG, fg=MUTED, font=(FONT, 11))
        self.hover.pack()

        # controls
        controls = tk.Frame(self.root, bg=BG, pady=8)
        controls.pack()
        tk.Label(controls, text="Difficulty:", bg=BG, fg=INK, font=(FONT, 12)).pack(side="left")
        self.difficulty = tk.StringVar(value=hunt.get_difficulty())
        menu = tk.OptionMenu(controls, self.difficulty, "easy", "normal", "hard")
        menu.configure(width=7)
        menu.pack(side="left", padx=(4, 12))
        tk.Button(controls, text="New game (N)", command=self.new_game).pack(side="left", padx=4)
        self.buy_button = tk.Button(
            controls, text=f"Buy shovel - {hunt.SHOVEL_COST_IN_COINS} coins (B)",
            command=self.buy_shovel,
        )
        self.buy_button.pack(side="left", padx=4)
        tk.Button(controls, text="Stats", command=self.show_stats).pack(side="left", padx=4)

        # legend
        legend = tk.Frame(self.root, bg=BG)
        legend.pack(pady=(0, 14))
        for text, color, fg in [("sand", SAND, INK), ("$ treasure", TREASURE, INK),
                                ("X trap", TRAP, "#ff6b6b"), ("burning", HINT_COLORS["burning"], "white"),
                                ("hot", HINT_COLORS["hot"], "white"), ("warm", HINT_COLORS["warm"], INK),
                                ("cold", HINT_COLORS["cold"], INK)]:
            tk.Label(legend, text=f" {text} ", bg=color, fg=fg,
                     font=(FONT, 10, "bold"), padx=4).pack(side="left", padx=3)

    def build_board(self, size):
        for child in self.board.winfo_children():
            child.destroy()
        self.cells = {}

        for c in range(size):
            tk.Label(self.board, text=LETTERS[c], bg=BG, fg=MUTED,
                     font=(FONT, 11, "bold")).grid(row=0, column=c + 1)
        for r in range(size):
            tk.Label(self.board, text=str(r + 1), bg=BG, fg=MUTED, width=3,
                     font=(FONT, 11, "bold")).grid(row=r + 1, column=0)
            for c in range(size):
                cell = tk.Label(self.board, width=3, height=1, bg=SAND, fg=INK,
                                font=(FONT, 14, "bold"), relief="raised", bd=2)
                cell.grid(row=r + 1, column=c + 1, padx=1, pady=1, ipady=4)
                cell.bind("<Button-1>", lambda e, r=r, c=c: self.dig(r, c))
                cell.bind("<Enter>", lambda e, r=r, c=c: self.on_hover(r, c, True))
                cell.bind("<Leave>", lambda e, r=r, c=c: self.on_hover(r, c, False))
                self.cells[(r, c)] = cell

        self.drawn_size = size

    # ---- drawing --------------------------------------------------------

    def refresh(self):
        state = hunt.get_state()
        if state["grid_size"] != self.drawn_size:
            self.build_board(state["grid_size"])

        for (r, c), label in self.cells.items():
            cell = state["grid"][r][c]
            if cell == "sand":
                label.configure(text="", bg=SAND, fg=INK, relief="raised",
                                cursor="hand2" if not state["over"] else "")
            elif cell == "empty":
                hint = self.hints.get((r, c))
                color = HINT_COLORS.get(hint, EMPTY)
                label.configure(text="", bg=color, relief="sunken", cursor="")
            elif cell == "treasure":
                label.configure(text="$", bg=TREASURE, fg="#7a4b00", relief="sunken", cursor="")
            elif cell == "trap":
                label.configure(text="X", bg=TRAP, fg="#ff6b6b", relief="sunken", cursor="")

        self.stat_labels["level"].configure(text=state["level"])
        self.stat_labels["shovels"].configure(text=state["shovels"],
                                              fg="#c92a2a" if state["shovels"] <= 3 else INK)
        self.stat_labels["coins"].configure(text=state["coins"])
        self.stat_labels["treasures_left"].configure(text=state["treasures_left"])
        self.stat_labels["streak"].configure(text=state["streak"])
        self.stat_labels["high"].configure(text=hunt.high_score())

        can_buy = not state["over"] and state["coins"] >= hunt.SHOVEL_COST_IN_COINS
        self.buy_button.configure(state="normal" if can_buy else "disabled")

    def say(self, text, result="info"):
        self.message.configure(text=text, fg=RESULT_COLORS.get(result, INK))

    def on_hover(self, r, c, entering):
        state = hunt.get_state()
        label = self.cells.get((r, c))
        if label is None or state["over"]:
            return
        if entering:
            self.hover.configure(text=f"{LETTERS[c]}{r + 1}")
        else:
            self.hover.configure(text=" ")
        if state["grid"][r][c] == "sand":
            label.configure(bg=SAND_HOVER if entering else SAND)

    # ---- actions --------------------------------------------------------

    def new_game(self):
        hunt.set_difficulty(self.difficulty.get())
        hunt.new_game()
        self.hints = {}
        self.old_high = hunt.high_score()
        self.old_achievements = set(hunt.get_stats()["achievements"])
        self.refresh()
        state = hunt.get_state()
        self.say(f"Level 1 on {self.difficulty.get()}: {state['treasures_left']} treasures, "
                 f"{state['shovels']} shovels. Start digging!")

    def dig(self, r, c):
        before = hunt.get_state()
        if before["over"]:
            return

        result = hunt.dig(r, c)
        after = hunt.get_state()

        if after["level"] > before["level"]:
            # new level, new grid - old hints mean nothing now
            self.hints = {}
        else:
            if result["hint"]:
                self.hints[(r, c)] = result["hint"]
            if result["result"] == "treasure":
                self.recheck_hints()

        self.say(result["message"], result["result"])
        self.refresh()

        if after["over"]:
            self.root.after(150, self.game_over)

    def recheck_hints(self):
        # once a treasure is dug up, older hints may point at it.
        # hunt.dig() on an already-dug square is free and returns a fresh hint.
        for (r, c) in list(self.hints):
            fresh = hunt.dig(r, c)
            if fresh["hint"]:
                self.hints[(r, c)] = fresh["hint"]

    def buy_shovel(self):
        result = hunt.buy_shovel()
        self.say(result["message"], "treasure" if result["ok"] else None)
        self.refresh()

    def game_over(self):
        state = hunt.get_state()
        lines = [f"You reached level {state['level']} with {state['coins']} coins."]
        if state["coins"] > self.old_high:
            lines.append(f"NEW HIGH SCORE: {hunt.high_score()}!")
        else:
            lines.append(f"High score: {hunt.high_score()}")

        new_ones = [a for a in hunt.get_stats()["achievements"] if a not in self.old_achievements]
        for key in new_ones:
            lines.append(f"Achievement unlocked: {ACHIEVEMENT_NAMES.get(key, (key,))[0]}")

        lines.append("")
        lines.append("Play again?")
        if messagebox.askyesno("Game over", "\n".join(lines), parent=self.root):
            self.new_game()
        else:
            self.say("Game over. Press New game when you're ready.", "trap")

    def show_stats(self):
        win = tk.Toplevel(self.root, bg=BG, padx=20, pady=16)
        win.title("Stats")
        win.resizable(False, False)
        stats = hunt.get_stats()

        def heading(text):
            tk.Label(win, text=text, bg=BG, fg=INK, font=(FONT, 14, "bold"),
                     anchor="w").pack(fill="x", pady=(10, 4))

        def line(left, right="", color=INK):
            row = tk.Frame(win, bg=BG)
            row.pack(fill="x")
            tk.Label(row, text=left, bg=BG, fg=color, font=(FONT, 12), anchor="w").pack(side="left")
            tk.Label(row, text=str(right), bg=BG, fg=color, font=(FONT, 12, "bold")).pack(side="right")

        heading("Lifetime")
        line("High score", stats["high_score"])
        line("Games played", stats["games_played"])
        line("Treasures found", stats["total_treasures_found"])
        line("Traps hit", stats["total_traps_hit"])
        line("Shovels used", stats["total_shovels_used"])
        line("Best level", stats["best_level"])

        heading("Leaderboard")
        board = hunt.get_leaderboard()
        if not board:
            line("No finished runs yet", color=MUTED)
        for i, entry in enumerate(board, start=1):
            line(f"{i}.  level {entry['level']}", f"{entry['coins']} coins")

        heading("Achievements")
        unlocked = set(stats["achievements"])
        for key, (title, desc) in ACHIEVEMENT_NAMES.items():
            if key in unlocked:
                line(f"[x] {title} - {desc}")
            else:
                line("[ ] ???", color=MUTED)

        tk.Button(win, text="Close", command=win.destroy).pack(pady=(14, 0))


def main():
    root = tk.Tk()
    TreasureGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()