# Project 96: Network Traffic & Socket Packet Analyzer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import socket
import struct
import threading
import tkinter as tk
from tkinter import ttk

is_sniffing = False


def parse_ip_header(data):
    # Extract first 20 bytes for IPv4 header
    ip_header = struct.unpack("!BBHHHBBH4s4s", data[:20])
    protocol = ip_header[6]
    src_ip = socket.inet_ntoa(ip_header[8])
    dst_ip = socket.inet_ntoa(ip_header[9])
    proto_name = {6: "TCP", 17: "UDP", 1: "ICMP"}.get(
        protocol, f"Proto-{protocol}"
    )
    return proto_name, src_ip, dst_ip


def simulate_packet_capture():
    # Production raw sockets require OS root privileges.
    # We implement a simulated stream inspector for clean, unprivileged portability.
    import random

    protocols = ["TCP", "UDP", "HTTPS", "DNS"]
    count = 0
    while is_sniffing:
        time_str = time.strftime("%H:%M:%S")
        proto = random.choice(protocols)
        src = f"192.168.1.{random.randint(2, 50)}"
        dst = f"10.0.0.{random.randint(1, 10)}"
        length = random.randint(64, 1500)
        tree.insert(
            "",
            tk.END,
            values=(count, time_str, proto, src, dst, f"{length} bytes"),
        )
        count += 1
        time.sleep(1)


import time


def toggle_sniffer():
    global is_sniffing
    if not is_sniffing:
        is_sniffing = True
        btn_toggle.config(text="Stop Sniffing", bg="#dc2626")
        threading.Thread(target=simulate_packet_capture, daemon=True).start()
    else:
        is_sniffing = False
        btn_toggle.config(text="Start Capture", bg="#2563eb")


root = tk.Tk()
root.title("Network Packet Analyzer")
root.geometry("640x420")
tk.Label(
    root,
    text="NETWORK TRAFFIC ANALYZER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=10)
btn_toggle = tk.Button(
    root,
    text="Start Capture",
    command=toggle_sniffer,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
)
btn_toggle.pack(pady=6)
tree = ttk.Treeview(
    root,
    columns=("No", "Time", "Protocol", "Source", "Destination", "Length"),
    show="headings",
    height=10,
)
tree.heading("No", text="No.")
tree.column("No", width=50, anchor="center")
tree.heading("Time", text="Time")
tree.column("Time", width=80, anchor="center")
tree.heading("Protocol", text="Protocol")
tree.column("Protocol", width=80, anchor="center")
tree.heading("Source", text="Source IP")
tree.column("Source", width=140)
tree.heading("Destination", text="Destination IP")
tree.column("Destination", width=140)
tree.heading("Length", text="Packet Size")
tree.column("Length", width=100, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
root.mainloop()
