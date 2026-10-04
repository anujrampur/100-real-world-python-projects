# Project 9: Random Quote Generator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import random

quotes = [
    {
        "quote": "The secret of getting ahead is getting started.",
        "author": "Mark Twain",
    },
    {
        "quote": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt",
    },
    {
        "quote": "It always seems impossible until it's done.",
        "author": "Nelson Mandela",
    },
    {
        "quote": "The best way to predict the future is to create it.",
        "author": "Peter Drucker",
    },
    {
        "quote": "Simplicity is prerequisite for reliability.",
        "author": "Edsger W. Dijkstra",
    },
    {
        "quote": "First, solve the problem. Then, write the code.",
        "author": "John Johnson",
    },
]


def show_quote():
    item = random.choice(quotes)
    quote_label.config(text=f'"{item["quote"]}"')
    author_label.config(text=f"- {item['author']}")


root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("500x320")
tk.Label(
    root, text="RANDOM QUOTE GENERATOR", font=("Arial", 16, "bold")
).pack(pady=15)
card_frame = tk.Frame(
    root, bg="#f7fafc", bd=1, relief="solid", padx=20, pady=20
)
card_frame.pack(fill="both", expand=True, padx=25, pady=10)
quote_label = tk.Label(
    card_frame,
    text="Click below to get inspired!",
    font=("Georgia", 13, "italic"),
    bg="#f7fafc",
    fg="#2d3748",
    wraplength=420,
    justify="center",
)
quote_label.pack(expand=True)
author_label = tk.Label(
    card_frame,
    text="",
    font=("Arial", 10, "bold"),
    bg="#f7fafc",
    fg="#4a5568",
)
author_label.pack(pady=5)
tk.Button(
    root,
    text="New Quote",
    command=show_quote,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
).pack(pady=15)
root.mainloop()
