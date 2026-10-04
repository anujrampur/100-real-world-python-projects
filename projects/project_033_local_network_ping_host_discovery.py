# Project 33: Local Network Ping & Host Discovery
# 100 Real-World Python Projects - Anuj Kumar Saxena
import subprocess
import platform
import threading
import re
import tkinter as tk
from tkinter import ttk, messagebox


def ping_host():
    host = host_entry.get().strip()
    if not host:
        messagebox.showerror("Error", "Enter a host name or IP address.")
        return
    btn_ping.config(state="disabled")
    status_label.config(text=f"Pinging {host}...", fg="#0284c7")
    output_text.delete("1.0", tk.END)

    def run():
        # -n 4 on Windows, -c 4 on UNIX
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "4", host]
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()
            output_text.insert(tk.END, stdout if stdout else stderr)
            if process.returncode == 0:
                # Extract latency
                times = re.findall(
                    r"time[=<](\d+\.?\d*)\s*ms", stdout, re.IGNORECASE
                )
                if times:
                    avg_time = sum(float(t) for t in times) / len(times)
                    status_label.config(
                        text=f"Host is UP! Average Latency: {avg_time:.1f} ms",
                        fg="#15803d",
                    )
                else:
                    status_label.config(
                        text="Host is UP! Reply received.", fg="#15803d"
                    )
            else:
                status_label.config(
                    text="Host is DOWN or unreachable.", fg="#dc2626"
                )
        except Exception as e:
            output_text.insert(tk.END, f"Execution failed: {e}")
            status_label.config(text="Ping execution error.", fg="#dc2626")
        btn_ping.config(state="normal")

    threading.Thread(target=run, daemon=True).start()


root = tk.Tk()
root.title("Network Ping Tool")
root.geometry("520x420")
tk.Label(
    root,
    text="NETWORK PING UTILITY",
    font=("Arial", 16, "bold"),
    fg="#0369a1",
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="Host / IP:").pack(side="left", padx=4)
host_entry = tk.Entry(f, width=26, font=("Arial", 10))
host_entry.pack(side="left", padx=4)
host_entry.insert(0, "8.8.8.8")
btn_ping = tk.Button(
    f,
    text="Ping Host",
    command=ping_host,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
)
btn_ping.pack(side="left", padx=5)
status_label = tk.Label(
    root,
    text="Enter host and click Ping",
    font=("Arial", 11, "bold"),
    fg="#64748b",
)
status_label.pack(pady=6)
output_text = tk.Text(
    root, height=14, width=60, font=("Consolas", 9), bg="#f8fafc"
)
output_text.pack(fill="both", expand=True, padx=20, pady=10)
root.mainloop()
