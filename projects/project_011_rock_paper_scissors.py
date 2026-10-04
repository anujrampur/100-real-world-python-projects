# Project 11: Rock Paper Scissors
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import random

choices = ["Rock", "Paper", "Scissors"]
user_score = 0
comp_score = 0


def play(user_choice):
    global user_score, comp_score
    comp_choice = random.choice(choices)
    if user_choice == comp_choice:
        outcome = f"It's a Tie! Both chose {user_choice}."
    elif (
        (user_choice == "Rock" and comp_choice == "Scissors")
        or (user_choice == "Paper" and comp_choice == "Rock")
        or (user_choice == "Scissors" and comp_choice == "Paper")
    ):
        user_score += 1
        outcome = f"You Win! {user_choice} beats {comp_choice}."
    else:
        comp_score += 1
        outcome = f"Computer Wins! {comp_choice} beats {user_choice}."
    result_label.config(text=outcome)
    score_label.config(
        text=f"Player: {user_score}  |  Computer: {comp_score}"
    )


def reset_game():
    global user_score, comp_score
    user_score = 0
    comp_score = 0
    score_label.config(text="Player: 0  |  Computer: 0")
    result_label.config(text="Choose your move to start!")


root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("450x330")
tk.Label(
    root, text="ROCK PAPER SCISSORS", font=("Arial", 18, "bold"), fg="#92400e"
).pack(pady=15)
score_label = tk.Label(
    root, text="Player: 0  |  Computer: 0", font=("Arial", 13, "bold")
)
score_label.pack(pady=5)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)
for move in choices:
    tk.Button(
        btn_frame,
        text=move,
        width=10,
        font=("Arial", 11, "bold"),
        command=lambda m=move: play(m),
    ).pack(side="left", padx=8)
result_label = tk.Label(
    root,
    text="Choose your move to start!",
    font=("Arial", 11),
    wraplength=380,
)
result_label.pack(pady=15)
tk.Button(root, text="Reset Score", command=reset_game, fg="#c53030").pack(
    pady=5
)
root.mainloop()
