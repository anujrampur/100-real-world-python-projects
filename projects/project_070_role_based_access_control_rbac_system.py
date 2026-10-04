# Project 70: Role-Based Access Control (RBAC) System
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import hashlib
import hmac
import secrets
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "rbac.db"


def hash_password(password, salt=None):
    """Return 'salt$hash' using salted PBKDF2-HMAC-SHA256."""
    salt = salt or secrets.token_hex(8)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100_000
    ).hex()
    return f"{salt}${digest}"


def verify_password(password, stored):
    salt = stored.split("$")[0]
    return hmac.compare_digest(hash_password(password, salt), stored)


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """)
    # Seed default roles and test users
    seed_users = [
        ("admin_user", hash_password("admin123"), "Admin"),
        ("editor_user", hash_password("edit123"), "Editor"),
        ("viewer_user", hash_password("view123"), "Viewer"),
    ]
    for u in seed_users:
        c.execute(
            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            u,
        )
    conn.commit()
    conn.close()


PERMISSIONS = {
    "Admin": ["Read", "Create", "Update", "Delete", "User Management"],
    "Editor": ["Read", "Create", "Update"],
    "Viewer": ["Read"],
}
active_user = None


def login():
    global active_user
    username = usr_entry.get().strip()
    pwd = pwd_entry.get().strip()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT role, password_hash FROM users WHERE username = ?",
        (username,),
    )
    found = c.fetchone()
    conn.close()
    row = found if found and verify_password(pwd, found[1]) else None
    if row:
        active_user = (username, row[0])
        status_lbl.config(
            text=f"Logged in as: {username} | Role: {row[0]}", fg="#15803d"
        )
        load_permissions(row[0])
    else:
        messagebox.showerror("Access Denied", "Invalid username or password.")


def check_permission(perm):
    if not active_user:
        messagebox.showerror("Denied", "Please log in first.")
        return
    role = active_user[1]
    if perm in PERMISSIONS.get(role, []):
        messagebox.showinfo(
            "Granted", f"Access GRANTED for operation: '{perm}'"
        )
    else:
        messagebox.showerror(
            "Denied",
            f"Access DENIED: Role '{role}' lacks '{perm}' permission.",
        )


def load_permissions(role):
    tree.delete(*tree.get_children())
    for perm in ["Read", "Create", "Update", "Delete", "User Management"]:
        has_perm = "ALLOW" if perm in PERMISSIONS.get(role, []) else "DENY"
        tree.insert("", tk.END, values=(perm, has_perm))


init_db()
root = tk.Tk()
root.title("RBAC Access Control Engine")
root.geometry("540x440")
tk.Label(
    root,
    text="ROLE-BASED ACCESS CONTROL (RBAC)",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=10)
# Login Frame
f_login = tk.Frame(root)
f_login.pack(pady=5)
tk.Label(f_login, text="User:").grid(row=0, column=0, padx=2)
usr_entry = tk.Entry(f_login, width=12)
usr_entry.grid(row=0, column=1, padx=4)
usr_entry.insert(0, "editor_user")
tk.Label(f_login, text="Pass:").grid(row=0, column=2, padx=2)
pwd_entry = tk.Entry(f_login, width=12, show="*")
pwd_entry.grid(row=0, column=3, padx=4)
pwd_entry.insert(0, "edit123")
tk.Button(
    f_login,
    text="Login",
    command=login,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).grid(row=0, column=4, padx=6)
status_lbl = tk.Label(
    root, text="Not logged in", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
tree = ttk.Treeview(
    root, columns=("Permission", "Status"), show="headings", height=5
)
tree.heading("Permission", text="System Permission")
tree.column("Permission", width=220)
tree.heading("Status", text="Authorization")
tree.column("Status", width=120, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=6)
# Test Action Buttons
btn_f = tk.Frame(root)
btn_f.pack(pady=8)
tk.Label(btn_f, text="Simulate Action:").pack(side="left", padx=4)
tk.Button(
    btn_f, text="Read Data", command=lambda: check_permission("Read")
).pack(side="left", padx=2)
tk.Button(
    btn_f,
    text="Delete Data",
    command=lambda: check_permission("Delete"),
    fg="#dc2626",
).pack(side="left", padx=2)
tk.Button(
    btn_f,
    text="Manage Users",
    command=lambda: check_permission("User Management"),
).pack(side="left", padx=2)
root.mainloop()
