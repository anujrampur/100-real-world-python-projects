# Project 15: Quiz Master
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox

QUESTIONS = [
    {
        "question": "Which data type is immutable in Python?",
        "options": ["List", "Dictionary", "Tuple", "Set"],
        "answer": 2,
    },
    {
        "question": "What is the output of 3 * 'A' in Python?",
        "options": ["AAA", "Error", "3A", "['A','A','A']"],
        "answer": 0,
    },
    {
        "question": "Which keyword is used to create a function?",
        "options": ["func", "def", "lambda", "define"],
        "answer": 1,
    },
    {
        "question": "What module handles JSON serialization in Python?",
        "options": ["xml", "json", "serialize", "pickle"],
        "answer": 1,
    },
]
current_q = 0
score = 0


def load_question():
    q_data = QUESTIONS[current_q]
    lbl_question.config(text=f"Q{current_q + 1}: {q_data['question']}")
    selected_option.set(-1)
    for idx, opt in enumerate(q_data["options"]):
        radio_buttons[idx].config(text=opt, value=idx)


def next_question():
    global current_q, score
    choice = selected_option.get()
    if choice == -1:
        messagebox.showwarning("Choice Required", "Please select an answer.")
        return
    if choice == QUESTIONS[current_q]["answer"]:
        score += 1
    current_q += 1
    if current_q < len(QUESTIONS):
        load_question()
    else:
        percent = (score / len(QUESTIONS)) * 100
        messagebox.showinfo(
            "Quiz Finished",
            f"Your Score: {score}/{len(QUESTIONS)} ({percent:.0f}%)",
        )
        restart_quiz()


def restart_quiz():
    global current_q, score
    current_q = 0
    score = 0
    load_question()


root = tk.Tk()
root.title("Quiz Master")
root.geometry("480x360")
tk.Label(
    root, text="PYTHON QUIZ MASTER", font=("Arial", 16, "bold"), fg="#92400e"
).pack(pady=15)
lbl_question = tk.Label(
    root, text="", font=("Arial", 12, "bold"), wraplength=420, justify="left"
)
lbl_question.pack(anchor="w", padx=30, pady=10)
selected_option = tk.IntVar(value=-1)
radio_buttons = []
for i in range(4):
    rb = tk.Radiobutton(
        root, text="", variable=selected_option, value=i, font=("Arial", 11)
    )
    rb.pack(anchor="w", padx=45, pady=3)
    radio_buttons.append(rb)
tk.Button(
    root,
    text="Next Question",
    command=next_question,
    bg="#d97706",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=5,
).pack(pady=20)
load_question()
root.mainloop()
