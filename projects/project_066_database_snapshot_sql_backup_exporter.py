# Project 66: Database Snapshot & SQL Backup Exporter
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def create_sample_db(filepath):
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS test_data (id INTEGER PRIMARY KEY, info TEXT)"
    )
    c.execute(
        "INSERT INTO test_data (info) VALUES ('Record 1'), ('Record 2'), ('Record 3')"
    )
    conn.commit()
    conn.close()


def live_backup():
    src_path = src_entry.get().strip()
    if not os.path.isfile(src_path):
        messagebox.showerror(
            "Error", "Select a valid source SQLite database file."
        )
        return
    dst_path = filedialog.asksaveasfilename(
        defaultextension=".db", filetypes=[("SQLite DB", "*.db")]
    )
    if not dst_path:
        return
    try:
        src_conn = sqlite3.connect(src_path)
        dst_conn = sqlite3.connect(dst_path)
        # Online non-blocking hot backup
        with dst_conn:
            src_conn.backup(dst_conn, pages=10)
        dst_conn.close()
        src_conn.close()
        messagebox.showinfo(
            "Success",
            f"Online backup completed successfully!\nSaved to: {dst_path}",
        )
    except Exception as e:
        messagebox.showerror("Backup Error", f"{e}")


def export_sql_dump():
    src_path = src_entry.get().strip()
    if not os.path.isfile(src_path):
        messagebox.showerror(
            "Error", "Select a valid source SQLite database file."
        )
        return
    dst_path = filedialog.asksaveasfilename(
        defaultextension=".sql", filetypes=[("SQL Dump", "*.sql")]
    )
    if not dst_path:
        return
    try:
        conn = sqlite3.connect(src_path)
        with open(dst_path, "w", encoding="utf-8") as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()
        messagebox.showinfo(
            "Success",
            f"SQL Dump exported successfully!\nSaved to: {dst_path}",
        )
    except Exception as e:
        messagebox.showerror("Dump Error", f"{e}")


SAMPLE_DB = "sample_data.db"
create_sample_db(SAMPLE_DB)
root = tk.Tk()
root.title("Database Snapshot & SQL Exporter")
root.geometry("520x260")
tk.Label(
    root,
    text="DATABASE SNAPSHOT & EXPORTER",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=15)
f = tk.Frame(root)
f.pack(pady=5)
src_entry = tk.Entry(f, width=38, font=("Arial", 9))
src_entry.pack(side="left", padx=4)
src_entry.insert(0, SAMPLE_DB)
tk.Button(
    f,
    text="Browse DB",
    command=lambda: src_entry.insert(0, filedialog.askopenfilename()),
).pack(side="left")
btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)
tk.Button(
    btn_frame,
    text="Live Binary Snapshot (.db)",
    command=live_backup,
    bg="#0891b2",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
).pack(side="left", padx=8)
tk.Button(
    btn_frame,
    text="Export SQL Dump (.sql)",
    command=export_sql_dump,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=5,
).pack(side="left", padx=8)
root.mainloop()
