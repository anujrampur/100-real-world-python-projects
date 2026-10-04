# Project 85: Single-Layer Perceptron Neural Network
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import ttk, messagebox


class Perceptron:
    def __init__(self, num_inputs=2, lr=0.1):
        self.weights = [0.0] * num_inputs
        self.bias = 0.0
        self.lr = lr

    def activate(self, x):
        return 1 if x >= 0.0 else 0

    def predict(self, inputs):
        dot_product = (
            sum(w * x for w, x in zip(self.weights, inputs)) + self.bias
        )
        return self.activate(dot_product)

    def train(self, training_data, epochs=50):
        for _ in range(epochs):
            for inputs, target in training_data:
                pred = self.predict(inputs)
                error = target - pred
                for i in range(len(self.weights)):
                    self.weights[i] += self.lr * error * inputs[i]
                self.bias += self.lr * error


AND_GATE = [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 1)]
OR_GATE = [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)]
p_model = Perceptron()


def train_gate():
    gate = gate_combo.get()
    data = AND_GATE if gate == "AND" else OR_GATE
    p_model.train(data, epochs=30)
    info_lbl.config(
        text=f"Trained {gate} Gate -> Weights: [{p_model.weights[0]:.2f}, {p_model.weights[1]:.2f}] | Bias: {p_model.bias:.2f}"
    )


def test_inference():
    try:
        a = int(in_a.get())
        b = int(in_b.get())
        if a not in [0, 1] or b not in [0, 1]:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Inputs must be binary integers (0 or 1)."
        )
        return
    res = p_model.predict([a, b])
    out_lbl.config(text=f"Perceptron Output: {res}")


root = tk.Tk()
root.title("Perceptron Neural Engine")
root.geometry("480x360")
tk.Label(
    root,
    text="SINGLE-LAYER PERCEPTRON",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f_tr = tk.Frame(root)
f_tr.pack(pady=5)
tk.Label(f_tr, text="Target Logic Gate:").pack(side="left", padx=4)
gate_combo = ttk.Combobox(
    f_tr, values=["AND", "OR"], width=6, state="readonly"
)
gate_combo.pack(side="left", padx=4)
gate_combo.set("AND")
tk.Button(
    f_tr,
    text="Train Perceptron",
    command=train_gate,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
info_lbl = tk.Label(
    root, text="Perceptron uninitialized", font=("Consolas", 9), fg="#475569"
)
info_lbl.pack(pady=6)
f_in = tk.Frame(root)
f_in.pack(pady=10)
tk.Label(f_in, text="Input A:").pack(side="left", padx=2)
in_a = tk.Entry(f_in, width=4, justify="center")
in_a.pack(side="left", padx=4)
in_a.insert(0, "1")
tk.Label(f_in, text="Input B:").pack(side="left", padx=2)
in_b = tk.Entry(f_in, width=4, justify="center")
in_b.pack(side="left", padx=4)
in_b.insert(0, "1")
tk.Button(f_in, text="Feedforward Infer", command=test_inference).pack(
    side="left", padx=6
)
out_lbl = tk.Label(
    root,
    text="Perceptron Output: --",
    font=("Arial", 12, "bold"),
    fg="#15803d",
)
out_lbl.pack(pady=15)
train_gate()
root.mainloop()
