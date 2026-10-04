# Project 71: Micro RESTful JSON API Server
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import urllib.parse
import json
import threading
import tkinter as tk
from tkinter import messagebox

ITEMS = {
    1: {"id": 1, "name": "Laptop", "price": 999.99},
    2: {"id": 2, "name": "Keyboard", "price": 49.99},
}


class RESTHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/items":
            self._send_json(200, list(ITEMS.values()))
        elif parsed.path.startswith("/api/items/"):
            try:
                item_id = int(parsed.path.split("/")[-1])
                if item_id in ITEMS:
                    self._send_json(200, ITEMS[item_id])
                else:
                    self._send_json(404, {"error": "Item not found"})
            except ValueError:
                self._send_json(400, {"error": "Invalid item ID"})
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if self.path == "/api/items":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length).decode("utf-8"))
                new_id = max(ITEMS.keys(), default=0) + 1
                body["id"] = new_id
                ITEMS[new_id] = body
                self._send_json(201, body)
            except Exception:
                self._send_json(400, {"error": "Malformed JSON payload"})
        else:
            self._send_json(404, {"error": "Endpoint not found"})


httpd = None


def start_server():
    global httpd
    try:
        httpd = socketserver.TCPServer(("127.0.0.1", 8081), RESTHandler)
        srv_status.config(
            text="API Server LIVE at http://127.0.0.1:8081/api/items",
            fg="#15803d",
        )
        btn_start.config(state="disabled")
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to bind port: {e}")


root = tk.Tk()
root.title("Micro REST API Server")
root.geometry("520x340")
tk.Label(
    root,
    text="MICRO RESTful API SERVICE",
    font=("Arial", 16, "bold"),
    fg="#1e3a8a",
).pack(pady=15)
srv_status = tk.Label(
    root, text="Server Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
srv_status.pack(pady=4)
btn_start = tk.Button(
    root,
    text="Start API Server (Port 8081)",
    command=start_server,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
)
btn_start.pack(pady=10)
routes_box = tk.Text(
    root, height=8, width=58, font=("Consolas", 9), bg="#f8fafc"
)
routes_box.pack(padx=20, pady=10)
routes_box.insert(
    tk.END,
    "Supported Endpoints:\n"
    "GET    /api/items          -> Retrieve all items\n"
    "GET    /api/items/<id>     -> Retrieve single item\n"
    "POST   /api/items          -> Create new item (JSON body)\n",
)
routes_box.config(state="disabled")
root.mainloop()
