# Project 14: Tic-Tac-Toe
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox

board = [""] * 9
current_player = "X"


def check_winner():
    combos = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # Rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # Columns
        (0, 4, 8),
        (2, 4, 6),  # Diagonals
    ]
    for a, b, c in combos:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Tie"
    return None


def on_click(index):
    global current_player
    if board[index] != "" or check_winner():
        return
    board[index] = current_player
    buttons[index].config(
        text=current_player,
        fg="#2563eb" if current_player == "X" else "#dc2626",
    )
    winner = check_winner()
    if winner:
        if winner == "Tie":
            messagebox.showinfo("Game Over", "It's a Draw!")
        else:
            messagebox.showinfo("Winner!", f"Player {winner} has won!")
        disable_all()
    else:
        current_player = "O" if current_player == "X" else "X"
        status_label.config(text=f"Player {current_player}'s Turn")


def disable_all():
    for btn in buttons:
        btn.config(state="disabled")


def reset_game():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    status_label.config(text="Player X's Turn")
    for btn in buttons:
        btn.config(text="", state="normal")


root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("380x420")
status_label = tk.Label(
    root, text="Player X's Turn", font=("Arial", 14, "bold"), fg="#92400e"
)
status_label.pack(pady=12)
grid_frame = tk.Frame(root)
grid_frame.pack()
buttons = []
for i in range(9):
    row, col = divmod(i, 3)
    btn = tk.Button(
        grid_frame,
        text="",
        font=("Arial", 22, "bold"),
        width=4,
        height=2,
        command=lambda idx=i: on_click(idx),
    )
    btn.grid(row=row, column=col, padx=4, pady=4)
    buttons.append(btn)
tk.Button(
    root,
    text="Restart Game",
    command=reset_game,
    font=("Arial", 11),
    padx=10,
    pady=4,
).pack(pady=15)
root.mainloop()
