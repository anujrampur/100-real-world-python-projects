# Project 16: Word Scramble
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import random

WORDS = [
    "PYTHON",
    "ALGORITHM",
    "PROGRAMMER",
    "COMPILER",
    "INTERFACE",
    "VARIABLE",
    "FUNCTION",
]
current_word = ""
score = 0


def scramble(word):
    chars = list(word)
    while True:
        shuffled = random.sample(chars, len(chars))
        if "".join(shuffled) != word:
            return "".join(shuffled)


def new_round():
    global current_word
    current_word = random.choice(WORDS)
    scrambled_label.config(text=scramble(current_word))
    entry_guess.delete(0, tk.END)
    hint_label.config(text="")


def check_word():
    global score
    guess = entry_guess.get().strip().upper()
    if guess == current_word:
        score += 10
        score_label.config(text=f"Score: {score}")
        messagebox.showinfo("Correct!", "Well done! +10 Points.")
        new_round()
    else:
        messagebox.showerror("Incorrect", "Try again or click for a hint!")


def give_hint():
    hint_label.config(
        text=f"Hint: First letter is '{current_word[0]}' and length is {len(current_word)}"
    )


root = tk.Tk()
root.title("Word Scramble")
root.geometry("450x360")
tk.Label(
    root, text="WORD SCRAMBLE", font=("Arial", 18, "bold"), fg="#92400e"
).pack(pady=15)
score_label = tk.Label(root, text="Score: 0", font=("Arial", 12, "bold"))
score_label.pack()
scrambled_label = tk.Label(
    root, text="", font=("Consolas", 24, "bold"), fg="#b45309"
)
scrambled_label.pack(pady=20)
entry_guess = tk.Entry(root, width=18, justify="center", font=("Arial", 14))
entry_guess.pack(pady=5)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(
    btn_frame,
    text="Submit",
    command=check_word,
    bg="#d97706",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
).pack(side="left", padx=4)
tk.Button(btn_frame, text="Hint", command=give_hint, padx=8).pack(
    side="left", padx=4
)
tk.Button(btn_frame, text="Skip Word", command=new_round, padx=8).pack(
    side="left", padx=4
)
hint_label = tk.Label(
    root, text="", font=("Arial", 10, "italic"), fg="#718096"
)
hint_label.pack(pady=8)
root.bind("<Return>", lambda e: check_word())
new_round()
root.mainloop()
