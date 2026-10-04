# Project 78: API Request Caching Layer with TTL Expiry
# 100 Real-World Python Projects - Anuj Kumar Saxena
import time
import hashlib
import json
import tkinter as tk
from tkinter import ttk, messagebox

CACHE_TTL_SECONDS = 10
cache_store = {}


def get_cache_key(endpoint: str, params: dict) -> str:
    serialized = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
    return hashlib.sha256(serialized.encode()).hexdigest()[:12]


def fetch_data(endpoint: str, params: dict):
    key = get_cache_key(endpoint, params)
    now = time.time()
    # Check cache hit
    if key in cache_store:
        entry = cache_store[key]
        if now - entry["cached_at"] < CACHE_TTL_SECONDS:
            remaining_ttl = int(
                CACHE_TTL_SECONDS - (now - entry["cached_at"])
            )
            return entry["data"], "CACHE HIT", remaining_ttl
    # Cache MISS - simulate remote backend fetch delay
    time.sleep(1.2)  # Simulated latency
    data = {
        "endpoint": endpoint,
        "params": params,
        "value": int(time.time() * 1000) % 10000,
    }
    cache_store[key] = {"data": data, "cached_at": now}
    return data, "CACHE MISS (Backend Queried)", CACHE_TTL_SECONDS


def request_api():
    param_val = param_entry.get().strip()
    status_lbl.config(text="Fetching...", fg="#0284c7")
    root.update_idletasks()
    data, status, ttl = fetch_data("/api/query", {"id": param_val})
    status_lbl.config(
        text=f"Result: {status} | TTL Remaining: {ttl}s",
        fg="#15803d" if "HIT" in status else "#b45309",
    )
    resp_text.delete("1.0", tk.END)
    resp_text.insert(tk.END, json.dumps(data, indent=4))
    refresh_cache_view()


def refresh_cache_view():
    tree.delete(*tree.get_children())
    now = time.time()
    for k, v in list(cache_store.items()):
        elapsed = now - v["cached_at"]
        rem = max(0, int(CACHE_TTL_SECONDS - elapsed))
        state = "Fresh" if rem > 0 else "Expired"
        tree.insert("", tk.END, values=(k, f"{rem}s", state))


root = tk.Tk()
root.title("API Request Cache Layer")
root.geometry("540x440")
tk.Label(
    root,
    text="API CACHING LAYER (TTL EXPIRY)",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=10)
f = tk.Frame(root)
f.pack(pady=4)
tk.Label(f, text="Query Param ID:").pack(side="left", padx=4)
param_entry = tk.Entry(f, width=10)
param_entry.pack(side="left", padx=4)
param_entry.insert(0, "user_42")
tk.Button(
    f,
    text="Execute Request",
    command=request_api,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
status_lbl = tk.Label(
    root, text="Ready", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
resp_text = tk.Text(
    root, height=4, width=54, font=("Consolas", 9), bg="#f8fafc"
)
resp_text.pack(padx=20, pady=4)
tk.Label(
    root, text="Active Cache Table (10s TTL):", font=("Arial", 9, "bold")
).pack(anchor="w", padx=20, pady=(8, 2))
tree = ttk.Treeview(
    root, columns=("Key", "TTL", "State"), show="headings", height=5
)
tree.heading("Key", text="Cache Key")
tree.column("Key", width=140, anchor="center")
tree.heading("TTL", text="TTL Remaining")
tree.column("TTL", width=120, anchor="center")
tree.heading("State", text="Cache State")
tree.column("State", width=120, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=4)
root.mainloop()
