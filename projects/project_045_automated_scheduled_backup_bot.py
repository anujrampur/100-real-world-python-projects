# Project 45: Automated Scheduled Backup Bot
# 100 Real-World Python Projects - Anuj Kumar Saxena
import zipfile
import os
import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

is_running = False


def create_backup(source_dir, dest_dir, max_backups=5):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.zip"
    archive_path = os.path.join(dest_dir, archive_name)
    # Create ZIP
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, source_dir)
                zipf.write(abs_path, rel_path)
    # Prune old backups
    existing = sorted(
        [
            f
            for f in os.listdir(dest_dir)
            if f.startswith("backup_") and f.endswith(".zip")
        ]
    )
    while len(existing) > max_backups:
        os.remove(os.path.join(dest_dir, existing.pop(0)))
    return archive_name


def backup_worker():
    src = src_entry.get().strip()
    dst = dst_entry.get().strip()
    while is_running:
        try:
            name = create_backup(src, dst)
            log_box.insert(
                tk.END,
                f"[{datetime.now().strftime('%H:%M:%S')}] Created: {name}\n",
            )
            log_box.see(tk.END)
        except Exception as e:
            log_box.insert(tk.END, f"[ERROR] Backup failed: {e}\n")
        # Sleep interval (default 30 seconds for test)
        for _ in range(30):
            if not is_running:
                break
            time.sleep(1)


def toggle_bot():
    global is_running
    src = src_entry.get().strip()
    dst = dst_entry.get().strip()
    if not os.path.isdir(src) or not os.path.isdir(dst):
        messagebox.showerror(
            "Error", "Select valid Source and Destination folders."
        )
        return
    if not is_running:
        is_running = True
        btn_toggle.config(text="Stop Backup Bot", bg="#dc2626")
        status_lbl.config(text="Status: Running (Every 30s)", fg="#15803d")
        threading.Thread(target=backup_worker, daemon=True).start()
    else:
        is_running = False
        btn_toggle.config(text="Start Backup Bot", bg="#b45309")
        status_lbl.config(text="Status: Stopped", fg="#64748b")


root = tk.Tk()
root.title("Scheduled Backup Bot")
root.geometry("520x440")
tk.Label(
    root,
    text="AUTOMATED BACKUP BOT",
    font=("Arial", 16, "bold"),
    fg="#7c2d12",
).pack(pady=12)
f1 = tk.Frame(root)
f1.pack(pady=4)
tk.Label(f1, text="Source Folder:").pack(anchor="w")
src_entry = tk.Entry(f1, width=40)
src_entry.pack(side="left", padx=4)
tk.Button(
    f1,
    text="Browse",
    command=lambda: src_entry.insert(0, filedialog.askdirectory()),
).pack(side="left")
f2 = tk.Frame(root)
f2.pack(pady=4)
tk.Label(f2, text="Backup Target Folder:").pack(anchor="w")
dst_entry = tk.Entry(f2, width=40)
dst_entry.pack(side="left", padx=4)
tk.Button(
    f2,
    text="Browse",
    command=lambda: dst_entry.insert(0, filedialog.askdirectory()),
).pack(side="left")
btn_toggle = tk.Button(
    root,
    text="Start Backup Bot",
    command=toggle_bot,
    bg="#b45309",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5,
)
btn_toggle.pack(pady=10)
status_lbl = tk.Label(
    root, text="Status: Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack()
log_box = tk.Text(
    root, height=10, width=58, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=10)
root.mainloop()
