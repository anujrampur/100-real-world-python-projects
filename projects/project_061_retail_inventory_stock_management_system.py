# Project 61: Retail Inventory & Stock Management System
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "inventory.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_product():
    name = name_entry.get().strip()
    cat = cat_entry.get().strip()
    try:
        qty = int(qty_entry.get())
        price = float(price_entry.get())
        if qty < 0 or price < 0 or not name:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Enter valid name, positive quantity, and price."
        )
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO products (name, category, quantity, unit_price) VALUES (?, ?, ?, ?)",
        (name, cat, qty, price),
    )
    conn.commit()
    conn.close()
    name_entry.delete(0, tk.END)
    cat_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    load_products()


def delete_product():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Select", "Select a product from the table.")
        return
    prod_id = tree.item(sel[0])["values"][0]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (prod_id,))
    conn.commit()
    conn.close()
    load_products()


def load_products():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, category, quantity, unit_price FROM products")
    rows = c.fetchall()
    conn.close()
    low_count = 0
    for row in rows:
        pid, name, cat, qty, price = row
        tree.insert("", tk.END, values=(pid, name, cat, qty, f"${price:.2f}"))
        if qty <= 5:
            low_count += 1
    status_lbl.config(
        text=f"Total Items: {len(rows)} | Low Stock Items (<= 5): {low_count}"
    )


init_db()
root = tk.Tk()
root.title("Retail Inventory Manager")
root.geometry("620x460")
tk.Label(
    root,
    text="RETAIL INVENTORY SYSTEM",
    font=("Arial", 16, "bold"),
    fg="#164e63",
).pack(pady=12)
f_in = tk.Frame(root)
f_in.pack(pady=5)
name_entry = tk.Entry(f_in, width=14)
name_entry.grid(row=0, column=0, padx=3)
cat_entry = tk.Entry(f_in, width=12)
cat_entry.grid(row=0, column=1, padx=3)
qty_entry = tk.Entry(f_in, width=6)
qty_entry.grid(row=0, column=2, padx=3)
price_entry = tk.Entry(f_in, width=8)
price_entry.grid(row=0, column=3, padx=3)
tk.Button(
    f_in,
    text="Add Product",
    command=add_product,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).grid(row=0, column=4, padx=4)
tk.Label(f_in, text="Name").grid(row=1, column=0)
tk.Label(f_in, text="Category").grid(row=1, column=1)
tk.Label(f_in, text="Qty").grid(row=1, column=2)
tk.Label(f_in, text="Price ($)").grid(row=1, column=3)
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Category", "Quantity", "Price"),
    show="headings",
    height=10,
)
tree.heading("ID", text="ID")
tree.column("ID", width=50, anchor="center")
tree.heading("Name", text="Product Name")
tree.column("Name", width=180)
tree.heading("Category", text="Category")
tree.column("Category", width=120)
tree.heading("Quantity", text="Quantity")
tree.column("Quantity", width=80, anchor="center")
tree.heading("Price", text="Unit Price")
tree.column("Price", width=90, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
b_frame = tk.Frame(root)
b_frame.pack(pady=5)
tk.Button(
    b_frame,
    text="Delete Selected",
    command=delete_product,
    bg="#dc2626",
    fg="white",
    padx=10,
).pack(side="left", padx=5)
status_lbl = tk.Label(root, text="", font=("Arial", 10, "bold"), fg="#0e7490")
status_lbl.pack(pady=4)
load_products()
root.mainloop()
