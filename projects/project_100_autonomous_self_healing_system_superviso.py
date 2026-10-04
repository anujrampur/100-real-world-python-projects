# Project 100: Autonomous Self-Healing System Supervisor & Watchdog
# 100 Real-World Python Projects - Anuj Kumar Saxena
import subprocess
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk

# Inline sample child worker script that intentionally runs or fails
WORKER_SCRIPT = """import time, sys
print("Worker service initialized.")
time.sleep(8)
print("Worker encountered simulated error! Exiting...")
sys.exit(1)
"""
with open("supervised_service.py", "w", encoding="utf-8") as f:
    f.write(WORKER_SCRIPT)
is_supervising = False
restart_count = 0


def supervisor_loop():
    global restart_count
    while is_supervising:
        log_event("[SUPERVISOR] Launching child service...")
        status_lbl.config(text="Status: SERVICE ACTIVE", fg="#15803d")
        # Spawn child service process
        proc = subprocess.Popen(
            [sys.executable, "supervised_service.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, _ = proc.communicate()
        if not is_supervising:
            break
        restart_count += 1
        log_event(
            f"[CRASH DETECTED] Process terminated with Exit Code: {proc.returncode}"
        )
        log_event(
            f"[SELF-HEALING] Restarting service automatically (Restart #{restart_count})..."
        )
        status_lbl.config(
            text=f"Status: RESTARTING (Recoveries: {restart_count})",
            fg="#dc2626",
        )
        time.sleep(2)


def log_event(msg):
    log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    log_box.see(tk.END)


def toggle_supervisor():
    global is_supervising
    if not is_supervising:
        is_supervising = True
        btn_start.config(text="Stop Supervisor", bg="#dc2626")
        threading.Thread(target=supervisor_loop, daemon=True).start()
    else:
        is_supervising = False
        btn_start.config(text="Start Watchdog Supervisor", bg="#2563eb")
        status_lbl.config(text="Status: SUPERVISOR INACTIVE", fg="#64748b")


root = tk.Tk()
root.title("Autonomous Self-Healing Supervisor")
root.geometry("580x420")
tk.Label(
    root,
    text="PROJECT 100: AUTONOMOUS SUPERVISOR",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=10)
status_lbl = tk.Label(
    root,
    text="Status: SUPERVISOR INACTIVE",
    font=("Arial", 11, "bold"),
    fg="#64748b",
)
status_lbl.pack(pady=4)
btn_start = tk.Button(
    root,
    text="Start Watchdog Supervisor",
    command=toggle_supervisor,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
)
btn_start.pack(pady=6)
log_box = tk.Text(
    root, height=13, width=64, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=8)
root.mainloop()
