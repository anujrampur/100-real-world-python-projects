# Project 7: Unit Conversion Toolkit
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import ttk, messagebox


def convert_length(value, source, target):
    factors = {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Mile": 1609.344,
        "Foot": 0.3048,
        "Inch": 0.0254,
    }
    return value * factors[source] / factors[target]


def convert_weight(value, source, target):
    factors = {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Pound": 0.45359237,
        "Ounce": 0.0283495231,
    }
    return value * factors[source] / factors[target]


def convert_temperature(value, source, target):
    if source == target:
        return value
    if source == "Celsius":
        c = value
    elif source == "Fahrenheit":
        c = (value - 32) * 5 / 9
    else:
        c = value - 273.15
    if target == "Celsius":
        return c
    elif target == "Fahrenheit":
        return c * 9 / 5 + 32
    return c + 273.15


def convert():
    try:
        value = float(value_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid number.")
        return
    category = category_combo.get()
    source = from_combo.get()
    target = to_combo.get()
    if category == "Length":
        res = convert_length(value, source, target)
    elif category == "Weight":
        res = convert_weight(value, source, target)
    else:
        res = convert_temperature(value, source, target)
    result_label.config(text=f"{value:g} {source} = {res:.4f} {target}")


root = tk.Tk()
root.title("Unit Conversion Toolkit")
root.geometry("480x380")
tk.Label(
    root, text="UNIT CONVERSION TOOLKIT", font=("Arial", 18, "bold")
).pack(pady=15)
category_combo = ttk.Combobox(
    root,
    values=["Length", "Weight", "Temperature"],
    state="readonly",
    width=20,
)
category_combo.pack(pady=5)
category_combo.set("Length")
value_entry = tk.Entry(root, width=20, justify="center")
value_entry.pack(pady=8)
value_entry.insert(0, "1")
units_frame = tk.Frame(root)
units_frame.pack(pady=5)
from_combo = ttk.Combobox(units_frame, state="readonly", width=14)
from_combo.pack(side="left", padx=6)
to_combo = ttk.Combobox(units_frame, state="readonly", width=14)
to_combo.pack(side="left", padx=6)


def update_units(event=None):
    category = category_combo.get()
    if category == "Length":
        units = ["Meter", "Kilometer", "Centimeter", "Mile", "Foot", "Inch"]
    elif category == "Weight":
        units = ["Kilogram", "Gram", "Pound", "Ounce"]
    else:
        units = ["Celsius", "Fahrenheit", "Kelvin"]
    from_combo["values"] = units
    to_combo["values"] = units
    from_combo.set(units[0])
    to_combo.set(units[1])


category_combo.bind("<<ComboboxSelected>>", update_units)
update_units()
tk.Button(
    root,
    text="Convert",
    command=convert,
    bg="#2563eb",
    fg="white",
    padx=12,
    pady=4,
).pack(pady=15)
result_label = tk.Label(
    root, text="", font=("Arial", 13, "bold"), fg="#1e3a8a"
)
result_label.pack(pady=10)
root.mainloop()
