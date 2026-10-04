# Project 84: Naive Bayes Text & Spam Filter
# 100 Real-World Python Projects - Anuj Kumar Saxena
import re
import math
import tkinter as tk
from tkinter import messagebox

TRAINING_DATA = [
    ("win cash prize claim your reward now", "spam"),
    ("exclusive free gift card click here to win", "spam"),
    ("urgent account notice verify secret password", "spam"),
    ("hello are we meeting for lunch tomorrow", "ham"),
    ("project documentation and code repository update", "ham"),
    ("please review the attached financial invoice and notes", "ham"),
]


class NaiveBayesSpam:
    def __init__(self):
        self.vocab = set()
        self.spam_counts = {}
        self.ham_counts = {}
        self.total_spam = 0
        self.total_ham = 0

    def tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    def fit(self, data):
        for msg, label in data:
            words = self.tokenize(msg)
            if label == "spam":
                self.total_spam += 1
                for w in words:
                    self.vocab.add(w)
                    self.spam_counts[w] = self.spam_counts.get(w, 0) + 1
            else:
                self.total_ham += 1
                for w in words:
                    self.vocab.add(w)
                    self.ham_counts[w] = self.ham_counts.get(w, 0) + 1

    def predict(self, text):
        words = self.tokenize(text)
        log_prob_spam = math.log(
            self.total_spam / (self.total_spam + self.total_ham)
        )
        log_prob_ham = math.log(
            self.total_ham / (self.total_spam + self.total_ham)
        )
        vocab_size = len(self.vocab)
        total_spam_words = sum(self.spam_counts.values())
        total_ham_words = sum(self.ham_counts.values())
        # Laplace smoothing (+1)
        for w in words:
            prob_w_spam = (self.spam_counts.get(w, 0) + 1) / (
                total_spam_words + vocab_size
            )
            prob_w_ham = (self.ham_counts.get(w, 0) + 1) / (
                total_ham_words + vocab_size
            )
            log_prob_spam += math.log(prob_w_spam)
            log_prob_ham += math.log(prob_w_ham)
        return "SPAM" if log_prob_spam > log_prob_ham else "HAM (LEGITIMATE)"


classifier = NaiveBayesSpam()
classifier.fit(TRAINING_DATA)


def check_message():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Enter text to classify.")
        return
    res = classifier.predict(text)
    res_lbl.config(
        text=f"Classification: {res}",
        fg="#dc2626" if "SPAM" in res else "#15803d",
    )


root = tk.Tk()
root.title("Naive Bayes Spam Filter")
root.geometry("520x360")
tk.Label(
    root,
    text="NAIVE BAYES TEXT CLASSIFIER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
input_text = tk.Text(root, height=5, width=54, font=("Arial", 10))
input_text.pack(padx=20, pady=5)
input_text.insert(tk.END, "Claim your free cash prize reward now!")
tk.Button(
    root,
    text="Classify Message",
    command=check_message,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
).pack(pady=10)
res_lbl = tk.Label(
    root, text="Classification: --", font=("Arial", 12, "bold"), fg="#1e3a8a"
)
res_lbl.pack(pady=5)
root.mainloop()
