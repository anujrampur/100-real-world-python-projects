# Project 18: Dice Battle Simulator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import random

DICE_GLYPHS = ["", " ", " ", " ", " ", " ", " "]
player_wins = 0
comp_wins = 0


def roll_dice():
    global player_wins, comp_wins
    p1, p2 = random.randint(1, 6), random.randint(1, 6)
    c1, c2 = random.randint(1, 6), random.randint(1, 6)
    p_total = p1 + p2
    c_total = c1 + c2
    p_dice_label.config(text=f"{DICE_GLYPHS[p1]} {DICE_GLYPHS[p2]}")
    c_dice_label.config(text=f"{DICE_GLYPHS[c1]} {DICE_GLYPHS[c2]}")
    if p_total > c_total:
        player_wins += 1
        verdict = f"Player Wins Round! ({p_total} vs {c_total})"
    elif c_total > p_total:
        comp_wins += 1
        verdict = f"Computer Wins Round! ({c_total} vs {p_total})"
    else:
        verdict = f"Tie Roll! Both rolled {p_total}"
    result_label.config(text=verdict)
    score_label.config(
        text=f"Player: {player_wins}  |  Computer: {comp_wins}"
    )


root = tk.Tk()
root.title("Dice Battle Simulator")
root.geometry("450x380")
tk.Label(
    root,
    text="DICE BATTLE SIMULATOR",
    font=("Arial", 16, "bold"),
    fg="#92400e",
).pack(pady=15)
score_label = tk.Label(
    root, text="Player: 0  |  Computer: 0", font=("Arial", 12, "bold")
)
score_label.pack()
board_frame = tk.Frame(root)
board_frame.pack(pady=20)
p_box = tk.Frame(board_frame, padx=15, pady=10, relief="groove", bd=2)
p_box.pack(side="left", padx=15)
tk.Label(p_box, text="You", font=("Arial", 11, "bold")).pack()
p_dice_label = tk.Label(p_box, text="   ", font=("Arial", 40), fg="#2563eb")
p_dice_label.pack()
c_box = tk.Frame(board_frame, padx=15, pady=10, relief="groove", bd=2)
c_box.pack(side="left", padx=15)
tk.Label(c_box, text="Computer", font=("Arial", 11, "bold")).pack()
c_dice_label = tk.Label(c_box, text="   ", font=("Arial", 40), fg="#dc2626")
c_dice_label.pack()
result_label = tk.Label(
    root, text="Click Roll to Battle!", font=("Arial", 11, "bold")
)
result_label.pack(pady=10)
tk.Button(
    root,
    text="Roll Dice!",
    command=roll_dice,
    bg="#d97706",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=5,
).pack(pady=10)
root.mainloop()
