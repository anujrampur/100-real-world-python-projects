# Project 49: Process Security & Keylogger Audit Tool
# 100 Real-World Python Projects - Anuj Kumar Saxena
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, messagebox

SUSPICIOUS_KEYWORDS = [
    "keylog",
    "hook",
    "spy",
    "inject",
    "sniff",
    "capture",
    "monitor",
    "stealth",
]


def audit_processes():
    tree.delete(*tree.get_children())
    os_type = platform.system().lower()
    suspicious_found = 0
    try:
        if os_type == "windows":
            out = subprocess.check_output(
                ["tasklist", "/FO", "CSV", "/NH"], text=True, errors="ignore"
            )
            lines = out.strip().split("\n")
            for line in lines:
                parts = [p.strip(' "') for p in line.split('","')]
                if len(parts) >= 2:
                    name, pid = parts[0], parts[1]
                    is_sus = any(
                        k in name.lower() for k in SUSPICIOUS_KEYWORDS
                    )
                    status = "WARNING" if is_sus else "Normal"
                    if is_sus:
                        suspicious_found += 1
                    tree.insert("", tk.END, values=(pid, name, status))
        else:
            out = subprocess.check_output(
                ["ps", "-eo", "pid,comm"], text=True, errors="ignore"
            )
            for line in out.strip().split("\n")[1:]:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    pid, name = parts[0], parts[1]
                    is_sus = any(
                        k in name.lower() for k in SUSPICIOUS_KEYWORDS
                    )
                    status = "WARNING" if is_sus else "Normal"
                    if is_sus:
                        suspicious_found += 1
                    tree.insert("", tk.END, values=(pid, name, status))
        status_lbl.config(
            text=f"Audit Complete: {suspicious_found} suspicious processes flagged.",
            fg="#dc2626" if suspicious_found else "#15803d",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Audit failed: {e}")


root = tk.Tk()
root.title("Process Security Audit")
root.geometry("520x440")
tk.Label(
    root,
    text="PROCESS AUDITOR & SECURITY CHECK",
    font=("Arial", 15, "bold"),
    fg="#7c2d12",
).pack(pady=12)
tree = ttk.Treeview(
    root, columns=("PID", "Process Name", "Risk"), show="headings", height=12
)
tree.heading("PID", text="PID")
tree.heading("Process Name", text="Executable Name")
tree.heading("Risk", text="Risk Status")
tree.column("PID", width=70, anchor="center")
tree.column("Process Name", width=280)
tree.column("Risk", width=100, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=5)
status_lbl = tk.Label(
    root, text="Ready to scan", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=6)
tk.Button(
    root,
    text="Audit Running Processes",
    command=audit_processes,
    bg="#b45309",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
).pack(pady=8)
audit_processes()
root.mainloop()
