# Project 69: JSON-to-Relational Normalizer & Importer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import json
import re
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "normalized.db"
SAMPLE_JSON = """[
    {"user_id": 101, "name": "Alice", "city": "New York", "active": 1},
    {"user_id": 102, "name": "Bob", "city": "London", "active": 0},
    {"user_id": 103, "name": "Charlie", "city": "Tokyo", "active": 1}
]"""


def normalize_and_import():
    raw = json_text.get("1.0", tk.END).strip()
    try:
        data = json.loads(raw)
        if not isinstance(data, list) or not data:
            raise ValueError(
                "Root element must be a non-empty JSON list of objects."
            )
    except Exception as e:
        messagebox.showerror("Invalid JSON", f"Failed to parse JSON: {e}")
        return
    # Extract dynamic schema keys
    keys = list(data[0].keys())
    # Identifiers cannot be passed as ? parameters, so validate them strictly
    for k in keys:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", str(k)):
            messagebox.showerror("Invalid key", f"Unsafe column name: {k!r}")
            return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create dynamic table based on keys
    cols_sql = ", ".join([f"{k} TEXT" for k in keys])
    c.execute("DROP TABLE IF EXISTS imported_records")
    c.execute(f"CREATE TABLE imported_records ({cols_sql})")
    # Ingest rows
    placeholders = ", ".join(["?"] * len(keys))
    for item in data:
        values = [str(item.get(k, "")) for k in keys]
        c.execute(
            f"INSERT INTO imported_records VALUES ({placeholders})", values
        )
    conn.commit()
    conn.close()
    messagebox.showinfo(
        "Success", f"Normalized and imported {len(data)} records!"
    )
    display_records(keys)


def display_records(keys):
    tree.delete(*tree.get_children())
    tree["columns"] = keys
    tree["show"] = "headings"
    for k in keys:
        tree.heading(k, text=k.title())
        tree.column(k, width=100, anchor="center")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM imported_records")
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()


root = tk.Tk()
root.title("JSON to Relational Normalizer")
root.geometry("560x480")
tk.Label(
    root,
    text="JSON-TO-RELATIONAL DATA NORMALIZER",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=10)
tk.Label(root, text="Input JSON Records (List of Objects):").pack(
    anchor="w", padx=20
)
json_text = tk.Text(root, height=8, width=58, font=("Consolas", 9))
json_text.pack(padx=20, pady=4)
json_text.insert(tk.END, SAMPLE_JSON)
tk.Button(
    root,
    text="Normalize & Import to SQLite",
    command=normalize_and_import,
    bg="#0891b2",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(pady=8)
tree = ttk.Treeview(root, height=6)
tree.pack(fill="both", expand=True, padx=20, pady=10)
root.mainloop()
