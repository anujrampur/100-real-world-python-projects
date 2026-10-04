# Project 68: Time-Series Metrics Logger & Query Engine
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import time
import random
import tkinter as tk
from tkinter import ttk

DB_NAME = "timeseries.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            timestamp INTEGER,
            metric_name TEXT,
            value REAL
        )
    """)
    c.execute(
        "CREATE INDEX IF NOT EXISTS idx_metrics_ts ON metrics(timestamp)"
    )
    conn.commit()
    conn.close()


def log_simulated_metric():
    ts = int(time.time())
    val = round(random.uniform(20.0, 95.0), 2)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO metrics (timestamp, metric_name, value) VALUES (?, 'CPU_Load', ?)",
        (ts, val),
    )
    conn.commit()
    conn.close()
    refresh_metrics()


def refresh_metrics():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT datetime(timestamp, 'unixepoch', 'localtime'), metric_name, value FROM metrics ORDER BY timestamp DESC LIMIT 20"
    )
    rows = c.fetchall()
    c.execute("SELECT AVG(value), MIN(value), MAX(value) FROM metrics")
    avg_v, min_v, max_v = c.fetchone()
    conn.close()
    for r in rows:
        tree.insert("", tk.END, values=r)
    if avg_v:
        stats_lbl.config(
            text=f"Historical Average: {avg_v:.2f}% | Min: {min_v:.2f}% | Max: {max_v:.2f}%"
        )


init_db()
root = tk.Tk()
root.title("Time-Series Metrics Storage")
root.geometry("540x400")
tk.Label(
    root,
    text="TIME-SERIES METRICS ENGINE",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=10)
tk.Button(
    root,
    text="+ Log Simulated Reading Now",
    command=log_simulated_metric,
    bg="#0891b2",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(pady=5)
tree = ttk.Treeview(
    root, columns=("Timestamp", "Metric", "Value"), show="headings", height=9
)
tree.heading("Timestamp", text="Timestamp (Local)")
tree.column("Timestamp", width=180)
tree.heading("Metric", text="Metric")
tree.column("Metric", width=120)
tree.heading("Value", text="Reading (%)")
tree.column("Value", width=90, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
stats_lbl = tk.Label(
    root,
    text="No metrics recorded yet",
    font=("Arial", 10, "bold"),
    fg="#0e7490",
)
stats_lbl.pack(pady=6)
refresh_metrics()
root.mainloop()
