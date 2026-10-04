# Project 4: BMI & Health Calculator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox


def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        if weight <= 0 or height_cm <= 0:
            raise ValueError
        height_m = height_cm / 100
        bmi = weight / (height_m**2)
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal Weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obesity"
        result.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
    except ValueError:
        messagebox.showerror(
            "Invalid Input", "Enter positive numeric values."
        )


root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x350")
tk.Label(
    root, text="BMI & Health Calculator", font=("Arial", 18, "bold")
).pack(pady=15)
tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root, width=20, justify="center")
weight_entry.pack(pady=5)
tk.Label(root, text="Height (cm)").pack()
height_entry = tk.Entry(root, width=20, justify="center")
height_entry.pack(pady=5)
tk.Button(
    root,
    text="Calculate BMI",
    command=calculate_bmi,
    bg="#2563eb",
    fg="white",
    padx=10,
    pady=4,
).pack(pady=15)
result = tk.Label(root, text="", font=("Arial", 13, "bold"))
result.pack(pady=10)
root.mainloop()
