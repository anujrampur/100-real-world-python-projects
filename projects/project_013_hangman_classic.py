# Project 13: Hangman Classic
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import random

WORDS = [
    "PYTHON",
    "ALGORITHM",
    "VARIABLE",
    "FUNCTION",
    "DEVELOPER",
    "DATABASE",
    "TKINTER",
]
GALLOWS = [
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
]
word = ""
guessed = set()
wrong_guesses = 0


def start_game():
    global word, guessed, wrong_guesses
    word = random.choice(WORDS)
    guessed = set()
    wrong_guesses = 0
    update_ui()
    entry_letter.focus()


def guess():
    global wrong_guesses
    char = entry_letter.get().strip().upper()
    entry_letter.delete(0, tk.END)
    if not char or len(char) != 1 or not char.isalpha():
        return
    if char in guessed:
        messagebox.showinfo("Already Guessed", f"You already tried '{char}'.")
        return
    guessed.add(char)
    if char not in word:
        wrong_guesses += 1
    update_ui()


def update_ui():
    gallows_label.config(text=GALLOWS[wrong_guesses])
    display_word = " ".join([c if c in guessed else "_" for c in word])
    word_label.config(text=display_word)
    guessed_label.config(text=f"Guessed: {', '.join(sorted(guessed))}")
    if all(c in guessed for c in word):
        messagebox.showinfo(
            "Victory!", f"Congratulations! The word was {word}!"
        )
        start_game()
    elif wrong_guesses >= len(GALLOWS) - 1:
        messagebox.showerror(
            "Game Over", f"You ran out of guesses! Word was {word}."
        )
        start_game()


root = tk.Tk()
root.title("Hangman Classic")
root.geometry("460x480")
tk.Label(
    root, text="HANGMAN CLASSIC", font=("Arial", 18, "bold"), fg="#92400e"
).pack(pady=10)
gallows_label = tk.Label(root, text="", font=("Courier", 11), justify="left")
gallows_label.pack(pady=5)
word_label = tk.Label(root, text="", font=("Arial", 20, "bold"))
word_label.pack(pady=10)
input_frame = tk.Frame(root)
input_frame.pack(pady=5)
entry_letter = tk.Entry(
    input_frame, width=5, justify="center", font=("Arial", 14)
)
entry_letter.pack(side="left", padx=5)
tk.Button(
    input_frame,
    text="Guess Letter",
    command=guess,
    bg="#d97706",
    fg="white",
    font=("Arial", 10, "bold"),
).pack(side="left")
guessed_label = tk.Label(root, text="", font=("Arial", 10), fg="#718096")
guessed_label.pack(pady=8)
tk.Button(root, text="Restart Game", command=start_game).pack(pady=5)
root.bind("<Return>", lambda e: guess())
start_game()
root.mainloop()
