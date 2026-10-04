# Project 63: Automated Double-Entry Accounting Ledger
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB_NAME = "ledger.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            name TEXT PRIMARY KEY,
            balance REAL DEFAULT 0.0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            description TEXT,
            debit_account TEXT,
            credit_account TEXT,
            amount REAL
        )
    """)
    # Seed standard chart of accounts
    for acc in ["Cash", "Revenue", "Equipment", "Accounts Payable"]:
        c.execute(
            "INSERT OR IGNORE INTO accounts (name, balance) VALUES (?, 0.0)",
            (acc,),
        )
    conn.commit()
    conn.close()


def record_transaction():
    desc = desc_entry.get().strip()
    debit = debit_combo.get()
    credit = credit_combo.get()
    try:
        amount = float(amount_entry.get())
        if amount <= 0 or debit == credit or not desc:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter valid description, amount > 0, and distinct accounts.",
        )
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        # Begin ACID atomic transaction
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO journal_entries (timestamp, description, debit_account, credit_account, amount) VALUES (?, ?, ?, ?, ?)",
            (ts, desc, debit, credit, amount),
        )
        c.execute(
            "UPDATE accounts SET balance = balance + ? WHERE name = ?",
            (amount, debit),
        )
        c.execute(
            "UPDATE accounts SET balance = balance - ? WHERE name = ?",
            (amount, credit),
        )
        conn.commit()
        messagebox.showinfo(
            "Success", "Transaction posted to general ledger!"
        )
    except Exception as e:
        conn.rollback()
        messagebox.showerror(
            "Transaction Error", f"Transaction rolled back: {e}"
        )
    finally:
        conn.close()
    desc_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    refresh_views()


def refresh_views():
    acc_tree.delete(*acc_tree.get_children())
    journal_tree.delete(*journal_tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, balance FROM accounts")
    for name, bal in c.fetchall():
        acc_tree.insert("", tk.END, values=(name, f"${bal:,.2f}"))
    c.execute(
        "SELECT timestamp, description, debit_account, credit_account, amount FROM journal_entries ORDER BY id DESC"
    )
    for row in c.fetchall():
        ts, desc, d_acc, c_acc, amt = row
        journal_tree.insert(
            "", tk.END, values=(ts, desc, d_acc, c_acc, f"${amt:,.2f}")
        )
    conn.close()


init_db()
root = tk.Tk()
root.title("General Ledger & Accounting System")
root.geometry("680x520")
tk.Label(
    root,
    text="GENERAL LEDGER (DOUBLE-ENTRY)",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=10)
f_in = tk.Frame(root)
f_in.pack(pady=5)
desc_entry = tk.Entry(f_in, width=16)
desc_entry.grid(row=0, column=0, padx=2)
amount_entry = tk.Entry(f_in, width=8)
amount_entry.grid(row=0, column=1, padx=2)
debit_combo = ttk.Combobox(
    f_in,
    values=["Cash", "Equipment", "Accounts Payable"],
    width=12,
    state="readonly",
)
debit_combo.grid(row=0, column=2, padx=2)
debit_combo.set("Cash")
credit_combo = ttk.Combobox(
    f_in,
    values=["Revenue", "Cash", "Accounts Payable"],
    width=12,
    state="readonly",
)
credit_combo.grid(row=0, column=3, padx=2)
credit_combo.set("Revenue")
tk.Button(
    f_in,
    text="Post Entry",
    command=record_transaction,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).grid(row=0, column=4, padx=4)
tk.Label(f_in, text="Description").grid(row=1, column=0)
tk.Label(f_in, text="Amount ($)").grid(row=1, column=1)
tk.Label(f_in, text="Debit Account").grid(row=1, column=2)
tk.Label(f_in, text="Credit Account").grid(row=1, column=3)
# Panes
panes = ttk.PanedWindow(root, orient="horizontal")
panes.pack(fill="both", expand=True, padx=15, pady=10)
# Accounts Table
f_left = tk.Frame(panes)
acc_tree = ttk.Treeview(
    f_left, columns=("Account", "Balance"), show="headings"
)
acc_tree.heading("Account", text="Account")
acc_tree.column("Account", width=110)
acc_tree.heading("Balance", text="Balance")
acc_tree.column("Balance", width=80, anchor="center")
acc_tree.pack(fill="both", expand=True)
panes.add(f_left, weight=1)
# Journal Table
f_right = tk.Frame(panes)
journal_tree = ttk.Treeview(
    f_right,
    columns=("Date", "Desc", "Debit", "Credit", "Amount"),
    show="headings",
)
journal_tree.heading("Date", text="Date")
journal_tree.column("Date", width=120)
journal_tree.heading("Desc", text="Description")
journal_tree.column("Desc", width=110)
journal_tree.heading("Debit", text="Debit")
journal_tree.column("Debit", width=70)
journal_tree.heading("Credit", text="Credit")
journal_tree.column("Credit", width=70)
journal_tree.heading("Amount", text="Amount")
journal_tree.column("Amount", width=70, anchor="center")
journal_tree.pack(fill="both", expand=True)
panes.add(f_right, weight=3)
refresh_views()
root.mainloop()
