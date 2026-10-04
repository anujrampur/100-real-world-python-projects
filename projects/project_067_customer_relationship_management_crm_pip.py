# Project 67: Customer Relationship Management (CRM) Pipeline
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "crm.db"
STAGES = ["Lead", "Contacted", "Proposal", "Won", "Lost"]


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            value REAL NOT NULL,
            stage TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_deal():
    client = client_entry.get().strip()
    stage = stage_combo.get()
    try:
        val = float(val_entry.get())
        if val <= 0 or not client:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Enter valid client name and positive deal value."
        )
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO deals (client_name, value, stage) VALUES (?, ?, ?)",
        (client, val, stage),
    )
    conn.commit()
    conn.close()
    client_entry.delete(0, tk.END)
    val_entry.delete(0, tk.END)
    load_deals()


def update_stage(new_stage):
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Select", "Select a deal from the pipeline.")
        return
    deal_id = tree.item(sel[0])["values"][0]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE deals SET stage = ? WHERE id = ?", (new_stage, deal_id))
    conn.commit()
    conn.close()
    load_deals()


def load_deals():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, client_name, value, stage FROM deals")
    rows = c.fetchall()
    total_pipeline = 0
    won_total = 0
    for r in rows:
        did, name, val, stage = r
        tree.insert("", tk.END, values=(did, name, f"${val:,.2f}", stage))
        total_pipeline += val
        if stage == "Won":
            won_total += val
    conn.close()
    stats_lbl.config(
        text=f"Total Pipeline: ${total_pipeline:,.2f} | Deals Won: ${won_total:,.2f}"
    )


init_db()
root = tk.Tk()
root.title("CRM Sales Pipeline Tracker")
root.geometry("620x460")
tk.Label(
    root, text="CRM SALES PIPELINE", font=("Arial", 16, "bold"), fg="#164e63"
).pack(pady=10)
f_in = tk.Frame(root)
f_in.pack(pady=5)
client_entry = tk.Entry(f_in, width=16)
client_entry.grid(row=0, column=0, padx=3)
val_entry = tk.Entry(f_in, width=8)
val_entry.grid(row=0, column=1, padx=3)
stage_combo = ttk.Combobox(f_in, values=STAGES, width=10, state="readonly")
stage_combo.grid(row=0, column=2, padx=3)
stage_combo.set("Lead")
tk.Button(
    f_in,
    text="Add Deal",
    command=add_deal,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).grid(row=0, column=3, padx=4)
tk.Label(f_in, text="Client Name").grid(row=1, column=0)
tk.Label(f_in, text="Value ($)").grid(row=1, column=1)
tk.Label(f_in, text="Pipeline Stage").grid(row=1, column=2)
tree = ttk.Treeview(
    root,
    columns=("ID", "Client", "Value", "Stage"),
    show="headings",
    height=9,
)
tree.heading("ID", text="ID")
tree.column("ID", width=50, anchor="center")
tree.heading("Client", text="Client Name")
tree.column("Client", width=200)
tree.heading("Value", text="Deal Value")
tree.column("Value", width=110, anchor="center")
tree.heading("Stage", text="Stage")
tree.column("Stage", width=120, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
stage_btn_frame = tk.Frame(root)
stage_btn_frame.pack(pady=4)
tk.Label(stage_btn_frame, text="Move Selected Deal to:").pack(
    side="left", padx=4
)
for s in STAGES:
    tk.Button(
        stage_btn_frame, text=s, command=lambda st=s: update_stage(st)
    ).pack(side="left", padx=2)
stats_lbl = tk.Label(root, text="", font=("Arial", 10, "bold"), fg="#0e7490")
stats_lbl.pack(pady=6)
load_deals()
root.mainloop()
