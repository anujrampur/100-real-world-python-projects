# Project 90: Multi-Layer Feedforward Neural Network
# 100 Real-World Python Projects - Anuj Kumar Saxena
import math
import tkinter as tk


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


class NeuralNetwork:
    def __init__(self):
        # 2 Input neurons -> 2 Hidden neurons -> 1 Output neuron
        self.w_hidden = [
            [0.5, -0.2],  # Weights to Hidden 1
            [0.8, 0.4],  # Weights to Hidden 2
        ]
        self.b_hidden = [0.1, -0.1]
        self.w_output = [0.7, -0.6]  # Weights from Hidden to Output
        self.b_output = 0.2

    def forward(self, inputs):
        # Layer 1: Hidden layer activations
        hidden_acts = []
        for i in range(2):
            z = (
                sum(w * x for w, x in zip(self.w_hidden[i], inputs))
                + self.b_hidden[i]
            )
            hidden_acts.append(sigmoid(z))
        # Layer 2: Output layer activation
        z_out = (
            sum(w * h for w, h in zip(self.w_output, hidden_acts))
            + self.b_output
        )
        return sigmoid(z_out), hidden_acts


nn = NeuralNetwork()


def run_forward():
    try:
        x1 = float(in_x1.get().strip())
        x2 = float(in_x2.get().strip())
    except ValueError:
        return
    out, h_acts = nn.forward([x1, x2])
    res_lbl.config(
        text=f"Network Output: {out:.4f}\n(Hidden Activations: H1={h_acts[0]:.3f}, H2={h_acts[1]:.3f})"
    )


root = tk.Tk()
root.title("Feedforward Neural Network")
root.geometry("480x320")
tk.Label(
    root,
    text="MULTI-LAYER NEURAL NETWORK (FORWARD PASS)",
    font=("Arial", 13, "bold"),
    fg="#1e3a8a",
).pack(pady=15)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="X1:").pack(side="left", padx=2)
in_x1 = tk.Entry(f, width=5, justify="center")
in_x1.pack(side="left", padx=4)
in_x1.insert(0, "0.5")
tk.Label(f, text="X2:").pack(side="left", padx=2)
in_x2 = tk.Entry(f, width=5, justify="center")
in_x2.pack(side="left", padx=4)
in_x2.insert(0, "0.8")
tk.Button(
    f,
    text="Compute Forward Pass",
    command=run_forward,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=8)
res_lbl = tk.Label(
    root,
    text="Network Output: --",
    font=("Consolas", 11, "bold"),
    fg="#15803d",
)
res_lbl.pack(pady=20)
run_forward()
root.mainloop()
