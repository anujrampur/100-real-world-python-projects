# Project 82: K-Nearest Neighbors (KNN) Classifier
# 100 Real-World Python Projects - Anuj Kumar Saxena
import math
import tkinter as tk
from tkinter import ttk, messagebox

# Sample dataset: [Feature1 (Size), Feature2 (Sweetness)], Class
TRAINING_DATA = [
    ([1.0, 8.0], "Apple"),
    ([2.0, 7.5], "Apple"),
    ([1.5, 9.0], "Apple"),
    ([8.0, 3.0], "Watermelon"),
    ([9.0, 2.5], "Watermelon"),
    ([8.5, 4.0], "Watermelon"),
    ([4.0, 5.0], "Orange"),
    ([5.0, 6.0], "Orange"),
]


def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def knn_classify(sample, k=3):
    distances = []
    for features, label in TRAINING_DATA:
        d = euclidean_distance(sample, features)
        distances.append((d, label))
    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]
    # Plurality voting
    votes = {}
    for _, label in k_nearest:
        votes[label] = votes.get(label, 0) + 1
    winner = max(votes.items(), key=lambda x: x[1])[0]
    return winner, k_nearest


def classify_input():
    try:
        f1 = float(f1_entry.get().strip())
        f2 = float(f2_entry.get().strip())
        k = int(k_combo.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid numeric feature values.")
        return
    predicted_class, neighbors = knn_classify([f1, f2], k=k)
    res_lbl.config(text=f"Predicted Class: {predicted_class}", fg="#15803d")
    tree.delete(*tree.get_children())
    for d, lbl in neighbors:
        tree.insert("", tk.END, values=(lbl, f"{d:.4f}"))


root = tk.Tk()
root.title("KNN Multi-Class Classifier")
root.geometry("520x420")
tk.Label(
    root,
    text="K-NEAREST NEIGHBORS (KNN) ENGINE",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f_in = tk.Frame(root)
f_in.pack(pady=5)
tk.Label(f_in, text="Size:").pack(side="left", padx=2)
f1_entry = tk.Entry(f_in, width=6, justify="center")
f1_entry.pack(side="left", padx=4)
f1_entry.insert(0, "2.2")
tk.Label(f_in, text="Sweetness:").pack(side="left", padx=2)
f2_entry = tk.Entry(f_in, width=6, justify="center")
f2_entry.pack(side="left", padx=4)
f2_entry.insert(0, "8.1")
tk.Label(f_in, text="K:").pack(side="left", padx=2)
k_combo = ttk.Combobox(
    f_in, values=["1", "3", "5"], width=4, state="readonly"
)
k_combo.pack(side="left", padx=4)
k_combo.set("3")
tk.Button(
    f_in,
    text="Classify",
    command=classify_input,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
res_lbl = tk.Label(
    root, text="Predicted Class: --", font=("Arial", 12, "bold"), fg="#1e3a8a"
)
res_lbl.pack(pady=10)
tree = ttk.Treeview(
    root, columns=("Neighbor", "Distance"), show="headings", height=4
)
tree.heading("Neighbor", text="Nearest Neighbor Label")
tree.column("Neighbor", width=200, anchor="center")
tree.heading("Distance", text="Euclidean Distance")
tree.column("Distance", width=140, anchor="center")
tree.pack(fill="both", expand=True, padx=30, pady=10)
classify_input()
root.mainloop()
