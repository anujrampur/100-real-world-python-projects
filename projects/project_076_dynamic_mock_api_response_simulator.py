# Project 76: Dynamic Mock API & Response Simulator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import time
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox

mock_config = {
    "status": 200,
    "delay": 0.0,
    "payload": {"status": "ok", "message": "Mock response successful"},
}


class MockHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(mock_config["delay"])
        self.send_response(mock_config["status"])
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(mock_config["payload"]).encode("utf-8"))


def apply_config():
    try:
        mock_config["status"] = int(status_combo.get())
        mock_config["delay"] = float(delay_entry.get().strip())
        mock_config["payload"] = json.loads(
            payload_text.get("1.0", tk.END).strip()
        )
        messagebox.showinfo("Success", "Mock API configuration updated!")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid configuration: {e}")


def start_server():
    server = socketserver.TCPServer(("127.0.0.1", 8084), MockHandler)
    srv_lbl.config(
        text="Mock Server LIVE at http://127.0.0.1:8084", fg="#15803d"
    )
    btn_start.config(state="disabled")
    threading.Thread(target=server.serve_forever, daemon=True).start()


root = tk.Tk()
root.title("Dynamic Mock API Simulator")
root.geometry("540x440")
tk.Label(
    root,
    text="DYNAMIC MOCK API SIMULATOR",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=10)
ctrl_f = tk.Frame(root)
ctrl_f.pack(pady=4)
tk.Label(ctrl_f, text="Status Code:").pack(side="left", padx=2)
status_combo = ttk.Combobox(
    ctrl_f,
    values=["200", "201", "400", "401", "404", "500", "503"],
    width=6,
    state="readonly",
)
status_combo.pack(side="left", padx=4)
status_combo.set("200")
tk.Label(ctrl_f, text="Latency Delay (sec):").pack(side="left", padx=4)
delay_entry = tk.Entry(ctrl_f, width=5)
delay_entry.pack(side="left", padx=4)
delay_entry.insert(0, "0.5")
tk.Button(
    ctrl_f,
    text="Update Rules",
    command=apply_config,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
tk.Label(root, text="Mock JSON Response Body:").pack(
    anchor="w", padx=20, pady=(6, 2)
)
payload_text = tk.Text(root, height=8, width=58, font=("Consolas", 9))
payload_text.pack(padx=20, pady=2)
payload_text.insert(tk.END, json.dumps(mock_config["payload"], indent=4))
f_srv = tk.Frame(root)
f_srv.pack(pady=10)
btn_start = tk.Button(
    f_srv,
    text="Start Mock Server (8084)",
    command=start_server,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
)
btn_start.pack(side="left", padx=5)
srv_lbl = tk.Label(
    f_srv, text="Server Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
srv_lbl.pack(side="left", padx=5)
root.mainloop()
