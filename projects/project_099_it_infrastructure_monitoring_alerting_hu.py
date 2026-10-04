# Project 99: IT Infrastructure Monitoring & Alerting Hub
# 100 Real-World Python Projects - Anuj Kumar Saxena
import shutil
import os
import platform
import time
import threading
import tkinter as tk
from tkinter import ttk

ALERT_DISK_THRESHOLD = 85  # Alert if disk usage exceeds 85%
is_monitoring = True


def check_metrics():
    # Disk Usage
    total, used, free = shutil.disk_usage("/")
    disk_pct = int((used / total) * 100)
    # Core count
    cores = os.cpu_count() or 1
    os_info = f"{platform.system()} {platform.release()}"
    is_alert = disk_pct >= ALERT_DISK_THRESHOLD
    return disk_pct, cores, os_info, is_alert


def monitor_loop():
    while is_monitoring:
        disk, cores, os_inf, alert = check_metrics()
        tree.delete(*tree.get_children())
        tree.insert("", tk.END, values=("Operating System", os_inf, "OK"))
        tree.insert("", tk.END, values=("CPU Logical Cores", cores, "OK"))
        status = "CRITICAL WARNING" if alert else "NORMAL"
        tree.insert(
            "", tk.END, values=("Disk Space Used", f"{disk}%", status)
        )
        if alert:
            alert_lbl.config(
                text=f"WARNING: Disk capacity high ({disk}%)!", fg="#dc2626"
            )
        else:
            alert_lbl.config(
                text="All Infrastructure Metrics Operational", fg="#15803d"
            )
        time.sleep(3)


root = tk.Tk()
root.title("IT Infrastructure Monitor")
root.geometry("560x360")
tk.Label(
    root,
    text="IT INFRASTRUCTURE MONITOR & ALERTING",
    font=("Arial", 14, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
tree = ttk.Treeview(
    root, columns=("Metric", "Value", "Status"), show="headings", height=5
)
tree.heading("Metric", text="Subsystem Metric")
tree.column("Metric", width=200)
tree.heading("Value", text="Current Reading")
tree.column("Value", width=180, anchor="center")
tree.heading("Status", text="Health Status")
tree.column("Status", width=120, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
alert_lbl = tk.Label(
    root,
    text="Evaluating metrics...",
    font=("Arial", 11, "bold"),
    fg="#0e7490",
)
alert_lbl.pack(pady=10)
threading.Thread(target=monitor_loop, daemon=True).start()
root.mainloop()
