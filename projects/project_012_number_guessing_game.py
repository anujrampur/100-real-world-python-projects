# Project 12: Number Guessing Game
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import random

target = random.randint(1, 100)
attempts = 0


def check_guess():
    global attempts
    try:
        guess = int(entry_guess.get())
        if guess < 1 or guess > 100:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Input", "Please enter a valid number between 1 and 100."
        )
        return
    attempts += 1
    if guess == target:
        feedback_label.config(
            text=f"Correct! Found in {attempts} attempts!", fg="#276749"
        )
        btn_guess.config(state="disabled")
    elif guess < target:
        feedback_label.config(
            text=f"Too Low! Guess higher than {guess}.", fg="#c05621"
        )
    else:
        feedback_label.config(
            text=f"Too High! Guess lower than {guess}.", fg="#c05621"
        )
    attempts_label.config(text=f"Attempts Used: {attempts}")
    entry_guess.delete(0, tk.END)


def new_game():
    global target, attempts
    target = random.randint(1, 100)
    attempts = 0
    feedback_label.config(
        text="Game started! Guess between 1 and 100.", fg="#2d3748"
    )
    attempts_label.config(text="Attempts Used: 0")
    btn_guess.config(state="normal")
    entry_guess.delete(0, tk.END)


root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("420x330")
tk.Label(
    root,
    text="NUMBER GUESSING GAME",
    font=("Arial", 16, "bold"),
    fg="#92400e",
).pack(pady=15)
feedback_label = tk.Label(
    root, text="Guess a number between 1 and 100:", font=("Arial", 11)
)
feedback_label.pack(pady=5)
entry_guess = tk.Entry(root, width=12, justify="center", font=("Arial", 14))
entry_guess.pack(pady=10)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
btn_guess = tk.Button(
    btn_frame,
    text="Submit Guess",
    command=check_guess,
    bg="#d97706",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
)
btn_guess.pack(side="left", padx=5)
tk.Button(btn_frame, text="New Game", command=new_game, padx=10, pady=4).pack(
    side="left", padx=5
)
attempts_label = tk.Label(
    root, text="Attempts Used: 0", font=("Arial", 10, "bold"), fg="#718096"
)
attempts_label.pack(pady=15)
root.bind("<Return>", lambda e: check_guess())
root.mainloop()
