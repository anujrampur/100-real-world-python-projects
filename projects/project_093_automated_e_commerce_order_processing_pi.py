# Project 93: Automated E-Commerce Order Processing Pipeline
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "ecommerce_orders.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            item TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()


def place_order():
    cust = cust_entry.get().strip()
    item = item_entry.get().strip()
    if not cust or not item:
        messagebox.showwarning("Warning", "Enter customer name and item.")
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (customer, item, status) VALUES (?, ?, 'PENDING')",
        (cust, item),
    )
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    cust_entry.delete(0, tk.END)
    item_entry.delete(0, tk.END)
    refresh_orders()
    # Trigger asynchronous processing pipeline
    threading.Thread(
        target=process_pipeline, args=(order_id,), daemon=True
    ).start()


def process_pipeline(order_id):
    stages = [
        "PAYMENT_VERIFIED",
        "INVENTORY_ALLOCATED",
        "PACKAGED",
        "DISPATCHED",
    ]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for stage in stages:
        time.sleep(1.5)  # Simulate pipeline work
        c.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (stage, order_id)
        )
        conn.commit()
    conn.close()


def refresh_orders():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, customer, item, status FROM orders ORDER BY id DESC LIMIT 15"
    )
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()
    root.after(1000, refresh_orders)


init_db()
root = tk.Tk()
root.title("E-Commerce Order Pipeline")
root.geometry("580x420")
tk.Label(
    root,
    text="AUTOMATED ORDER PROCESSING PIPELINE",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f_in = tk.Frame(root)
f_in.pack(pady=5)
tk.Label(f_in, text="Customer:").pack(side="left", padx=2)
cust_entry = tk.Entry(f_in, width=14)
cust_entry.pack(side="left", padx=4)
cust_entry.insert(0, "Alice Smith")
tk.Label(f_in, text="Item:").pack(side="left", padx=2)
item_entry = tk.Entry(f_in, width=14)
item_entry.pack(side="left", padx=4)
item_entry.insert(0, "Gaming Monitor")
tk.Button(
    f_in,
    text="Submit Order",
    command=place_order,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
tree = ttk.Treeview(
    root,
    columns=("ID", "Customer", "Item", "Status"),
    show="headings",
    height=9,
)
tree.heading("ID", text="Order ID")
tree.column("ID", width=70, anchor="center")
tree.heading("Customer", text="Customer")
tree.column("Customer", width=160)
tree.heading("Item", text="Item Purchased")
tree.column("Item", width=160)
tree.heading("Status", text="Pipeline Status")
tree.column("Status", width=140, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
refresh_orders()
root.mainloop()
