# Project 17: Memory Matching Cards
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import random

ICONS = ["A", "B", "C", "D", "E", "F", "G", "H"] * 2
random.shuffle(ICONS)
first_card = None
second_card = None
lock_board = False
matches_found = 0
moves = 0


def card_click(index):
    global first_card, second_card, lock_board, matches_found, moves
    if lock_board or buttons[index]["text"] != "?":
        return
    buttons[index].config(text=ICONS[index], bg="#fed7aa")
    if first_card is None:
        first_card = index
    else:
        second_card = index
        moves += 1
        moves_label.config(text=f"Moves: {moves}")
        if ICONS[first_card] == ICONS[second_card]:
            buttons[first_card].config(bg="#bbf7d0")
            buttons[second_card].config(bg="#bbf7d0")
            first_card = None
            second_card = None
            matches_found += 1
            if matches_found == len(ICONS) // 2:
                messagebox.showinfo(
                    "Victory!", f"Completed in {moves} moves!"
                )
        else:
            lock_board = True
            root.after(800, hide_cards)


def hide_cards():
    global first_card, second_card, lock_board
    buttons[first_card].config(text="?", bg="#f3f4f6")
    buttons[second_card].config(text="?", bg="#f3f4f6")
    first_card = None
    second_card = None
    lock_board = False


root = tk.Tk()
root.title("Memory Matching Cards")
root.geometry("420x460")
tk.Label(
    root, text="MEMORY MATCHING", font=("Arial", 16, "bold"), fg="#92400e"
).pack(pady=10)
moves_label = tk.Label(root, text="Moves: 0", font=("Arial", 11, "bold"))
moves_label.pack(pady=4)
grid_frame = tk.Frame(root)
grid_frame.pack(pady=10)
buttons = []
for i in range(16):
    row, col = divmod(i, 4)
    btn = tk.Button(
        grid_frame,
        text="?",
        font=("Arial", 16, "bold"),
        width=4,
        height=2,
        bg="#f3f4f6",
        command=lambda idx=i: card_click(idx),
    )
    btn.grid(row=row, column=col, padx=4, pady=4)
    buttons.append(btn)
root.mainloop()
