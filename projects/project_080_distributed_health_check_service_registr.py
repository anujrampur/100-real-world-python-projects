# Project 80: Distributed Health Check & Service Registry Hub
# 100 Real-World Python Projects - Anuj Kumar Saxena
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

REGISTRY = {}
reg_lock = threading.Lock()
HEARTBEAT_TIMEOUT = 6  # Seconds before service is marked DEAD


def register_service(name: str, host: str, port: int):
    with reg_lock:
        REGISTRY[name] = {
            "host": host,
            "port": port,
            "last_heartbeat": time.time(),
            "status": "HEALTHY",
        }


def send_heartbeat(name: str):
    with reg_lock:
        if name in REGISTRY:
            REGISTRY[name]["last_heartbeat"] = time.time()
            REGISTRY[name]["status"] = "HEALTHY"


def health_checker():
    while True:
        now = time.time()
        with reg_lock:
            for name, data in REGISTRY.items():
                if now - data["last_heartbeat"] > HEARTBEAT_TIMEOUT:
                    data["status"] = "UNHEALTHY (CRITICAL)"
        time.sleep(2)


# Start background health evaluation thread
threading.Thread(target=health_checker, daemon=True).start()
# Seed mock microservices
register_service("Auth-Service", "127.0.0.1", 8081)
register_service("Payment-Gateway", "127.0.0.1", 8082)
register_service("Notification-Worker", "127.0.0.1", 8083)


def ping_selected():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning(
            "Select", "Select a service to send heartbeat."
        )
        return
    svc_name = tree.item(sel[0])["values"][0]
    send_heartbeat(svc_name)
    refresh_ui()


def refresh_ui():
    tree.delete(*tree.get_children())
    with reg_lock:
        for name, data in REGISTRY.items():
            tree.insert(
                "",
                tk.END,
                values=(
                    name,
                    f"{data['host']}:{data['port']}",
                    data["status"],
                ),
            )
    root.after(1000, refresh_ui)


root = tk.Tk()
root.title("Microservice Registry & Health Hub")
root.geometry("580x400")
tk.Label(
    root,
    text="SERVICE REGISTRY & DISCOVERY HUB",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
tk.Label(
    root,
    text="Heartbeat timeout: 6s. Click 'Send Heartbeat' to keep a service alive.",
    font=("Arial", 9),
).pack()
tree = ttk.Treeview(
    root, columns=("Service", "Address", "Health"), show="headings", height=8
)
tree.heading("Service", text="Service Name")
tree.column("Service", width=180)
tree.heading("Address", text="Host / Port")
tree.column("Address", width=150, anchor="center")
tree.heading("Health", text="Health Status")
tree.column("Health", width=180, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
btn_f = tk.Frame(root)
btn_f.pack(pady=6)
tk.Button(
    btn_f,
    text="Send Heartbeat Ping (+6s)",
    command=ping_selected,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(side="left", padx=4)
refresh_ui()
root.mainloop()
