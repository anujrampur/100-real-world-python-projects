# Project 8: Personal Password Generator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import string
import secrets


def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4 or length > 100:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Length", "Use a length between 4 and 100."
        )
        return
    chars = ""
    if lower_var.get():
        chars += string.ascii_lowercase
    if upper_var.get():
        chars += string.ascii_uppercase
    if number_var.get():
        chars += string.digits
    if symbol_var.get():
        chars += string.punctuation
    if not chars:
        messagebox.showwarning(
            "Selection Required", "Select at least one character type."
        )
        return
    password = "".join(secrets.choice(chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def copy_password():
    pwd = password_entry.get()
    if not pwd:
        messagebox.showwarning("No Password", "Generate a password first.")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard!")


root = tk.Tk()
root.title("Password Generator")
root.geometry("450x420")
tk.Label(root, text="PASSWORD GENERATOR", font=("Arial", 18, "bold")).pack(
    pady=15
)
tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root, width=10, justify="center")
length_entry.pack(pady=5)
length_entry.insert(0, "16")
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)
chk_frame = tk.Frame(root)
chk_frame.pack(pady=10)
tk.Checkbutton(chk_frame, text="Lowercase (a-z)", variable=lower_var).pack(
    anchor="w"
)
tk.Checkbutton(chk_frame, text="Uppercase (A-Z)", variable=upper_var).pack(
    anchor="w"
)
tk.Checkbutton(chk_frame, text="Numbers (0-9)", variable=number_var).pack(
    anchor="w"
)
tk.Checkbutton(
    chk_frame, text="Special Symbols (!@#$)", variable=symbol_var
).pack(anchor="w")
password_entry = tk.Entry(
    root, width=32, justify="center", font=("Consolas", 12)
)
password_entry.pack(pady=15)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(
    btn_frame,
    text="Generate",
    command=generate_password,
    bg="#2563eb",
    fg="white",
    padx=10,
    pady=4,
).pack(side="left", padx=6)
tk.Button(
    btn_frame,
    text="Copy to Clipboard",
    command=copy_password,
    padx=10,
    pady=4,
).pack(side="left", padx=6)
root.mainloop()
