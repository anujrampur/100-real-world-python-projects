# Project 29: System Resource Monitor
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import ttk
import shutil
import platform
import os


def update_metrics():
    # Disk Usage
    total, used, free = shutil.disk_usage("/")
    disk_percent = int((used / total) * 100)
    disk_bar["value"] = disk_percent
    disk_label.config(
        text=f"Disk Usage: {disk_percent}% ({used//(2**30)} GB / {total//(2**30)} GB)"
    )
    # System Info
    cpu_count = os.cpu_count() or 1
    sys_info = f"OS: {platform.system()} {platform.release()} | Architecture: {platform.machine()}"
    info_label.config(text=sys_info)
    cores_label.config(text=f"Logical CPU Cores Available: {cpu_count}")
    root.after(2000, update_metrics)


root = tk.Tk()
root.title("System Resource Monitor")
root.geometry("460x320")
tk.Label(
    root,
    text="SYSTEM RESOURCE MONITOR",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=15)
info_label = tk.Label(root, text="", font=("Arial", 9), fg="#4a5568")
info_label.pack(pady=2)
cores_label = tk.Label(
    root, text="", font=("Arial", 10, "bold"), fg="#1e293b"
)
cores_label.pack(pady=5)
monitor_frame = tk.Frame(root, padx=20, pady=10)
monitor_frame.pack(fill="both", expand=True)
disk_label = tk.Label(
    monitor_frame,
    text="Disk Usage: Calculating...",
    font=("Arial", 10, "bold"),
    anchor="w",
)
disk_label.pack(fill="x", pady=4)
disk_bar = ttk.Progressbar(
    monitor_frame, orient="horizontal", length=380, mode="determinate"
)
disk_bar.pack(pady=5)
root.after(200, update_metrics)
root.mainloop()
