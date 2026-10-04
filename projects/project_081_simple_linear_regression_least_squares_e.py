# Project 81: Simple Linear Regression & Least Squares Engine
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox


class LinearRegression:
    def __init__(self):
        self.m = 0.0  # Slope
        self.c = 0.0  # Y-intercept
        self.r2 = 0.0  # R-squared

    def fit(self, x, y):
        n = len(x)
        if n < 2:
            raise ValueError("At least 2 points required.")
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        # Calculate slope (m) and intercept (c)
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        if denominator == 0:
            raise ZeroDivisionError("Vertical line; variance of X is zero.")
        self.m = numerator / denominator
        self.c = mean_y - (self.m * mean_x)
        # Calculate R-squared
        ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
        ss_res = sum((y[i] - (self.m * x[i] + self.c)) ** 2 for i in range(n))
        self.r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

    def predict(self, val):
        return (self.m * val) + self.c


model = LinearRegression()
x_points = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
y_points = [2.2, 3.8, 6.1, 7.9, 10.2, 12.1]
model.fit(x_points, y_points)


def train_and_predict():
    try:
        val = float(input_entry.get().strip())
        pred = model.predict(val)
        result_lbl.config(text=f"Prediction for X = {val:g}: Y ≈ {pred:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid numeric value for X.")


root = tk.Tk()
root.title("Linear Regression Engine")
root.geometry("480x360")
tk.Label(
    root,
    text="ORDINARY LEAST SQUARES REGRESSION",
    font=("Arial", 14, "bold"),
    fg="#1e3a8a",
).pack(pady=15)
summary_box = tk.Label(
    root,
    text=f"Fitted Line: Y = {model.m:.2f}X + {model.c:.2f}\nGoodness of Fit (R²): {model.r2:.4f}",
    font=("Consolas", 11),
    bg="#f8fafc",
    bd=1,
    relief="solid",
    padx=15,
    pady=10,
)
summary_box.pack(pady=10)
f = tk.Frame(root)
f.pack(pady=10)
tk.Label(f, text="Input Independent Feature X:").pack(side="left", padx=4)
input_entry = tk.Entry(f, width=10, justify="center")
input_entry.pack(side="left", padx=4)
input_entry.insert(0, "7.5")
tk.Button(
    f,
    text="Predict Y",
    command=train_and_predict,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
result_lbl = tk.Label(
    root,
    text="Click Predict Y to infer target",
    font=("Arial", 11, "bold"),
    fg="#15803d",
)
result_lbl.pack(pady=15)
root.mainloop()
