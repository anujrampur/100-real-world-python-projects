# Project 86: Decision Tree Binary Rule Classifier
# 100 Real-World Python Projects - Anuj Kumar Saxena
import math
import tkinter as tk
from tkinter import ttk

# Dataset: [Outlook, Humidity], PlayTennis?
DATA = [
    (["Sunny", "High"], "No"),
    (["Sunny", "Normal"], "Yes"),
    (["Rainy", "High"], "No"),
    (["Rainy", "Normal"], "Yes"),
]


def entropy(labels):
    n = len(labels)
    counts = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1
    ent = 0.0
    for count in counts.values():
        p = count / n
        ent -= p * math.log2(p)
    return ent


def find_best_split():
    base_ent = entropy([row[1] for row in DATA])
    # Compute split for feature 0 (Outlook)
    left = [row[1] for row in DATA if row[0][0] == "Sunny"]
    right = [row[1] for row in DATA if row[0][0] == "Rainy"]
    info_gain = base_ent - (
        len(left) / len(DATA) * entropy(left)
        + len(right) / len(DATA) * entropy(right)
    )
    return f"Base Entropy: {base_ent:.3f} | Split on 'Outlook' -> Gain: {info_gain:.3f}"


root = tk.Tk()
root.title("Decision Tree Rule Engine")
root.geometry("500x340")
tk.Label(
    root,
    text="DECISION TREE SPLIT ENGINE",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
rule_box = tk.Label(
    root,
    text="Constructed Decision Rule:\nIF Humidity == 'Normal' -> Play = 'Yes'\nELSE IF Humidity == 'High' -> Play = 'No'",
    font=("Consolas", 11),
    bg="#f8fafc",
    bd=1,
    relief="solid",
    padx=15,
    pady=12,
)
rule_box.pack(pady=10)
stat_lbl = tk.Label(
    root, text=find_best_split(), font=("Arial", 10, "bold"), fg="#0e7490"
)
stat_lbl.pack(pady=8)
root.mainloop()
