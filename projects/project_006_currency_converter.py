# Project 6: Currency Converter
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import ttk, messagebox

RATES = {
    "USD": 1.00,
    "INR": 83.50,
    "EUR": 0.92,
    "GBP": 0.78,
    "JPY": 149.00,
    "AUD": 1.52,
    "CAD": 1.36,
}


def convert_currency():
    try:
        amount = float(amount_entry.get())
        if amount < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Amount", "Enter a valid non-negative number."
        )
        return
    source = from_combo.get()
    target = to_combo.get()
    usd = amount / RATES[source]
    result = usd * RATES[target]
    result_label.config(
        text=f"{amount:,.2f} {source} = {result:,.2f} {target}"
    )


root = tk.Tk()
root.title("Currency Converter")
root.geometry("450x330")
tk.Label(root, text="CURRENCY CONVERTER", font=("Arial", 18, "bold")).pack(
    pady=15
)
amount_entry = tk.Entry(root, width=20, justify="center")
amount_entry.pack(pady=8)
amount_entry.insert(0, "100")
currencies = list(RATES.keys())
frame = tk.Frame(root)
frame.pack(pady=10)
from_combo = ttk.Combobox(
    frame, values=currencies, state="readonly", width=10
)
from_combo.pack(side="left", padx=10)
from_combo.set("USD")
to_combo = ttk.Combobox(frame, values=currencies, state="readonly", width=10)
to_combo.pack(side="left", padx=10)
to_combo.set("INR")
tk.Button(
    root,
    text="Convert",
    command=convert_currency,
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
