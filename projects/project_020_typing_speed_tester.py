# Project 20: Typing Speed Tester
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import time
import random

PARAGRAPHS = [
    "Python is an interpreted, high-level and general-purpose programming language designed for readability.",
    "Clean code always looks like it was written by someone who cares and values simplicity.",
    "Functions should do one thing, they should do it well, and they should do it only.",
    "Programs must be written for people to read, and only incidentally for machines to execute.",
]
target_text = ""
start_time = None
is_running = False


def start_test():
    global target_text, start_time, is_running
    target_text = random.choice(PARAGRAPHS)
    passage_label.config(text=target_text)
    entry_text.delete("1.0", tk.END)
    entry_text.config(state="normal")
    entry_text.focus()
    stats_label.config(text="Start typing above to start the timer!")
    start_time = None
    is_running = False


def on_key(event):
    global start_time, is_running
    if not is_running:
        start_time = time.perf_counter()
        is_running = True
    typed = entry_text.get("1.0", tk.END).strip()
    elapsed = max(time.perf_counter() - start_time, 0.1)
    # Calculate WPM & Accuracy
    words = len(typed.split())
    wpm = int((words / elapsed) * 60)
    correct_chars = sum(
        1
        for i, c in enumerate(typed)
        if i < len(target_text) and c == target_text[i]
    )
    total_typed = max(len(typed), 1)
    accuracy = int((correct_chars / total_typed) * 100)
    stats_label.config(
        text=f"Time: {elapsed:.1f}s  |  Speed: {wpm} WPM  |  Accuracy: {accuracy}%"
    )
    if typed == target_text:
        entry_text.config(state="disabled")
        stats_label.config(
            text=f"Completed! Final: {wpm} WPM | Accuracy: {accuracy}% in {elapsed:.1f}s"
        )


root = tk.Tk()
root.title("Typing Speed Tester")
root.geometry("550x380")
tk.Label(
    root, text="TYPING SPEED TESTER", font=("Arial", 16, "bold"), fg="#92400e"
).pack(pady=15)
passage_label = tk.Label(
    root,
    text="",
    font=("Georgia", 11, "italic"),
    wraplength=480,
    justify="left",
    fg="#334155",
)
passage_label.pack(pady=10, padx=20)
entry_text = tk.Text(
    root, height=4, width=50, font=("Arial", 11), wrap="word"
)
entry_text.pack(pady=10)
entry_text.bind("<KeyRelease>", on_key)
stats_label = tk.Label(
    root,
    text="Click Start Test to begin!",
    font=("Arial", 10, "bold"),
    fg="#0f766e",
)
stats_label.pack(pady=10)
tk.Button(
    root,
    text="Start Test / Reset",
    command=start_test,
    bg="#d97706",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
).pack(pady=5)
root.mainloop()
