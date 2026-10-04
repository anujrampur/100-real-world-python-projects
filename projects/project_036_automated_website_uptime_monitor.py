# Project 36: Automated Website Uptime Monitor
# 100 Real-World Python Projects - Anuj Kumar Saxena
import urllib.request
import urllib.error
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

SITES = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    "https://httpstat.us/404",
    "https://httpstat.us/500",
]
is_monitoring = False


def check_site(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            latency = int((time.perf_counter() - start) * 1000)
            return resp.status, f"{latency} ms", "ONLINE"
    except urllib.error.HTTPError as e:
        latency = int((time.perf_counter() - start) * 1000)
        return e.code, f"{latency} ms", "ERROR"
    except Exception:
        return "FAIL", "--", "OFFLINE"


def monitor_loop():
    while is_monitoring:
        results = []
        for site in SITES:
            status, lat, state = check_site(site)
            results.append((site, status, lat, state))
        # Update table
        tree.delete(*tree.get_children())
        for r in results:
            tree.insert("", tk.END, values=r)
        time.sleep(10)  # Check every 10 seconds


def toggle_monitor():
    global is_monitoring
    if not is_monitoring:
        is_monitoring = True
        btn_toggle.config(text="Stop Monitoring", bg="#dc2626")
        status_lbl.config(
            text="Status: Active (Checking every 10s)", fg="#15803d"
        )
        threading.Thread(target=monitor_loop, daemon=True).start()
    else:
        is_monitoring = False
        btn_toggle.config(text="Start Monitoring", bg="#0284c7")
        status_lbl.config(text="Status: Paused", fg="#64748b")


def add_url():
    new_url = entry_url.get().strip()
    if new_url.startswith(("http://", "https://")) and new_url not in SITES:
        SITES.append(new_url)
        entry_url.delete(0, tk.END)
        messagebox.showinfo("Added", f"Added {new_url} to monitor list.")


root = tk.Tk()
root.title("Website Uptime Monitor")
root.geometry("560x420")
tk.Label(
    root,
    text="UPTIME & SERVICE HEALTH MONITOR",
    font=("Arial", 16, "bold"),
    fg="#0369a1",
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=5)
entry_url = tk.Entry(f, width=32, font=("Arial", 10))
entry_url.pack(side="left", padx=4)
entry_url.insert(0, "https://en.wikipedia.org")
tk.Button(f, text="Add Website", command=add_url).pack(side="left")
btn_toggle = tk.Button(
    root,
    text="Start Monitoring",
    command=toggle_monitor,
    bg="#0284c7",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=4,
)
btn_toggle.pack(pady=8)
status_lbl = tk.Label(
    root, text="Status: Paused", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack()
tree = ttk.Treeview(
    root,
    columns=("URL", "Status", "Latency", "State"),
    show="headings",
    height=8,
)
tree.heading("URL", text="Target URL")
tree.heading("Status", text="HTTP Code")
tree.heading("Latency", text="Latency")
tree.heading("State", text="State")
tree.column("URL", width=250)
tree.column("Status", width=90, anchor="center")
tree.column("Latency", width=90, anchor="center")
tree.column("State", width=90, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
root.mainloop()
