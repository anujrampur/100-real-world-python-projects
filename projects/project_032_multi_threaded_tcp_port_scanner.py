# Project 32: Multi-Threaded TCP Port Scanner
# 100 Real-World Python Projects - Anuj Kumar Saxena
import socket
import threading
from queue import Queue
import tkinter as tk
from tkinter import ttk, messagebox

port_queue = Queue()
open_ports = []
is_scanning = False
COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
}


def scan_worker(target):
    while not port_queue.empty():
        port = port_queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.6)
            result = s.connect_ex((target, port))
            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown")
                open_ports.append((port, service))
            s.close()
        except:
            pass
        port_queue.task_done()


def start_scan_thread():
    target = target_entry.get().strip()
    if not target:
        messagebox.showerror("Error", "Enter a valid target host or IP.")
        return
    tree.delete(*tree.get_children())
    open_ports.clear()
    status_label.config(text=f"Scanning {target}...", fg="#0284c7")
    btn_scan.config(state="disabled")

    def run():
        # Scan ports 1 to 1024
        for p in range(1, 1025):
            port_queue.put(p)
        threads = []
        for _ in range(50):  # 50 concurrent worker threads
            t = threading.Thread(
                target=scan_worker, args=(target,), daemon=True
            )
            t.start()
            threads.append(t)
        port_queue.join()
        # Update GUI on completion
        for p, s in sorted(open_ports):
            tree.insert("", tk.END, values=(p, "Open", s))
        status_label.config(
            text=f"Scan Finished. {len(open_ports)} open port(s) found.",
            fg="#15803d",
        )
        btn_scan.config(state="normal")

    threading.Thread(target=run, daemon=True).start()


root = tk.Tk()
root.title("TCP Port Scanner")
root.geometry("480x420")
tk.Label(
    root, text="TCP PORT SCANNER", font=("Arial", 16, "bold"), fg="#0369a1"
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="Target Host / IP:").pack(side="left", padx=4)
target_entry = tk.Entry(f, width=22, font=("Arial", 10))
target_entry.pack(side="left", padx=4)
target_entry.insert(0, "127.0.0.1")
btn_scan = tk.Button(
    f,
    text="Start Scan",
    command=start_scan_thread,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=8,
)
btn_scan.pack(side="left", padx=5)
status_label = tk.Label(
    root, text="Ready to scan (Ports 1 - 1024)", font=("Arial", 10)
)
status_label.pack(pady=5)
tree = ttk.Treeview(
    root, columns=("Port", "State", "Service"), show="headings", height=10
)
tree.heading("Port", text="Port")
tree.heading("State", text="State")
tree.heading("Service", text="Service")
tree.column("Port", width=90, anchor="center")
tree.column("State", width=110, anchor="center")
tree.column("Service", width=180, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
root.mainloop()
