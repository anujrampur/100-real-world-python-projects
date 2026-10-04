# Project 95: Cryptographic File Sync & Mirroring Daemon
# 100 Real-World Python Projects - Anuj Kumar Saxena
import os
import shutil
import hashlib
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

is_syncing = False


def compute_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(32 * 1024):
            h.update(chunk)
    return h.hexdigest()


def sync_directories(src, dst):
    log = []
    os.makedirs(dst, exist_ok=True)
    src_files = {}
    for root, _, files in os.walk(src):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, src)
            src_files[rel_path] = compute_hash(full_path)
    # Sync additions and modifications
    for rel_path, h_src in src_files.items():
        src_path = os.path.join(src, rel_path)
        dst_path = os.path.join(dst, rel_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        if not os.path.exists(dst_path) or compute_hash(dst_path) != h_src:
            shutil.copy2(src_path, dst_path)
            log.append(f"[COPIED] {rel_path}")
    # Remove deleted files from destination
    for root, _, files in os.walk(dst):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, dst)
            if rel_path not in src_files:
                os.remove(full_path)
                log.append(f"[DELETED] {rel_path}")
    return log


def sync_daemon():
    src = src_entry.get().strip()
    dst = dst_entry.get().strip()
    while is_syncing:
        try:
            changes = sync_directories(src, dst)
            if changes:
                for c in changes:
                    log_box.insert(tk.END, c + "\n")
                log_box.see(tk.END)
        except Exception as e:
            log_box.insert(tk.END, f"[SYNC ERROR] {e}\n")
        time.sleep(3)


def toggle_sync():
    global is_syncing
    src = src_entry.get().strip()
    dst = dst_entry.get().strip()
    if not os.path.isdir(src) or not dst:
        messagebox.showerror(
            "Error", "Select valid Source and Target folders."
        )
        return
    if not is_syncing:
        is_syncing = True
        btn_toggle.config(text="Stop Mirroring", bg="#dc2626")
        status_lbl.config(
            text="Daemon Active (Checking every 3s)", fg="#15803d"
        )
        threading.Thread(target=sync_daemon, daemon=True).start()
    else:
        is_syncing = False
        btn_toggle.config(text="Start Sync Daemon", bg="#2563eb")
        status_lbl.config(text="Daemon Stopped", fg="#64748b")


root = tk.Tk()
root.title("Cryptographic File Sync Daemon")
root.geometry("540x420")
tk.Label(
    root,
    text="CRYPTOGRAPHIC FILE MIRRORING DAEMON",
    font=("Arial", 14, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f1 = tk.Frame(root)
f1.pack(pady=4)
tk.Label(f1, text="Source:").pack(side="left", padx=2)
src_entry = tk.Entry(f1, width=38)
src_entry.pack(side="left", padx=4)
tk.Button(
    f1,
    text="Browse",
    command=lambda: src_entry.insert(0, filedialog.askdirectory()),
).pack(side="left")
f2 = tk.Frame(root)
f2.pack(pady=4)
tk.Label(f2, text="Mirror:").pack(side="left", padx=2)
dst_entry = tk.Entry(f2, width=38)
dst_entry.pack(side="left", padx=4)
tk.Button(
    f2,
    text="Browse",
    command=lambda: dst_entry.insert(0, filedialog.askdirectory()),
).pack(side="left")
btn_toggle = tk.Button(
    root,
    text="Start Sync Daemon",
    command=toggle_sync,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
)
btn_toggle.pack(pady=8)
status_lbl = tk.Label(
    root, text="Daemon Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=2)
log_box = tk.Text(
    root, height=10, width=58, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=8)
root.mainloop()
