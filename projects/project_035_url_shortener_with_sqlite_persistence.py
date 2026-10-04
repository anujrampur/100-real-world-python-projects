# Project 35: URL Shortener with SQLite Persistence
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "urls.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT,
            clicks INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def shorten_url():
    long_url = url_entry.get().strip()
    if not long_url.startswith(("http://", "https://")):
        messagebox.showerror(
            "Error", "Enter a valid URL starting with http:// or https://"
        )
        return
    # Create 6-character hash key
    short_code = hashlib.md5(long_url.encode()).hexdigest()[:6]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO urls (short_code, long_url, clicks) VALUES (?, ?, 0)",
            (short_code, long_url),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already exists
    conn.close()
    result_entry.delete(0, tk.END)
    result_entry.insert(0, f"http://short.ly/{short_code}")
    load_history()


def simulate_visit():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning(
            "Select Link", "Select a link from the table to simulate a visit."
        )
        return
    short_code = tree.item(sel[0])["values"][0]
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
        (short_code,),
    )
    conn.commit()
    conn.close()
    load_history()


def load_history():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT short_code, long_url, clicks FROM urls ORDER BY id DESC"
    )
    for row in c.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()


init_db()
root = tk.Tk()
root.title("URL Shortener & Database")
root.geometry("520x460")
tk.Label(
    root,
    text="URL SHORTENER & ANALYTICS",
    font=("Arial", 16, "bold"),
    fg="#0369a1",
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="Long URL:").pack(anchor="w")
url_entry = tk.Entry(f, width=42, font=("Arial", 10))
url_entry.pack(side="left", padx=4)
url_entry.insert(0, "https://www.python.org/downloads/release/python-3120/")
tk.Button(
    f,
    text="Shorten",
    command=shorten_url,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
).pack(side="left")
f_res = tk.Frame(root)
f_res.pack(pady=8)
tk.Label(f_res, text="Generated Short URL:").pack(side="left", padx=4)
result_entry = tk.Entry(
    f_res, width=28, font=("Arial", 10, "bold"), fg="#0369a1"
)
result_entry.pack(side="left", padx=4)
tree = ttk.Treeview(
    root, columns=("Short", "Target URL", "Clicks"), show="headings", height=8
)
tree.heading("Short", text="Short Code")
tree.heading("Target URL", text="Original URL")
tree.heading("Clicks", text="Clicks")
tree.column("Short", width=90, anchor="center")
tree.column("Target URL", width=300)
tree.column("Clicks", width=60, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(
    btn_frame, text="Simulate Click (+1)", command=simulate_visit, padx=10
).pack(side="left", padx=5)
load_history()
root.mainloop()
