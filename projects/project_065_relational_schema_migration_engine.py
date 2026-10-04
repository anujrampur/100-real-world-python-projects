# Project 65: Relational Schema Migration Engine
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "app_production.db"
MIGRATIONS = [
    (
        1,
        "Create Users Table",
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL);",
        "DROP TABLE users;",
    ),
    (
        2,
        "Add Email Column to Users",
        "ALTER TABLE users ADD COLUMN email TEXT;",
        "-- SQLite ALTER DROP COLUMN requires recreate",
    ),
    (
        3,
        "Create Profiles Table",
        "CREATE TABLE profiles (id INTEGER PRIMARY KEY, user_id INTEGER, bio TEXT);",
        "DROP TABLE profiles;",
    ),
]


def init_migration_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT,
            applied_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_current_version():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT MAX(version) FROM schema_migrations")
    val = c.fetchone()[0]
    conn.close()
    return val if val is not None else 0


def apply_next_migration():
    cur = get_current_version()
    next_m = None
    for m in MIGRATIONS:
        if m[0] == cur + 1:
            next_m = m
            break
    if not next_m:
        messagebox.showinfo("Status", "Database schema is fully up to date!")
        return
    ver, name, up_sql, _ = next_m
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute(up_sql)
        c.execute(
            "INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, datetime('now'))",
            (ver, name),
        )
        conn.commit()
        messagebox.showinfo("Success", f"Applied migration {ver}: {name}")
    except Exception as e:
        conn.rollback()
        messagebox.showerror(
            "Migration Failed", f"Error applying migration: {e}"
        )
    finally:
        conn.close()
    refresh_ui()


def refresh_ui():
    cur_v = get_current_version()
    ver_lbl.config(text=f"Current Database Version: v{cur_v}")
    tree.delete(*tree.get_children())
    for ver, name, up, down in MIGRATIONS:
        status = "Applied" if ver <= cur_v else "Pending"
        tree.insert("", tk.END, values=(f"v{ver}", name, status))


init_migration_table()
root = tk.Tk()
root.title("Schema Migration Engine")
root.geometry("540x360")
tk.Label(
    root,
    text="DATABASE SCHEMA MIGRATION ENGINE",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=12)
ver_lbl = tk.Label(
    root, text="Current Version: v0", font=("Arial", 11, "bold"), fg="#0e7490"
)
ver_lbl.pack(pady=4)
tree = ttk.Treeview(
    root,
    columns=("Version", "Migration Name", "Status"),
    show="headings",
    height=6,
)
tree.heading("Version", text="Version")
tree.column("Version", width=80, anchor="center")
tree.heading("Migration Name", text="Migration Name")
tree.column("Migration Name", width=280)
tree.heading("Status", text="Status")
tree.column("Status", width=90, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
tk.Button(
    root,
    text="Apply Next Migration (UP)",
    command=apply_next_migration,
    bg="#0891b2",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
).pack(pady=10)
refresh_ui()
root.mainloop()
