# Project 92: Distributed API Gateway & Load Balancer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import urllib.request
import threading
import itertools
import tkinter as tk

BACKENDS = ["http://127.0.0.1:8081", "http://127.0.0.1:8082"]
backend_pool = itertools.cycle(BACKENDS)
routing_log = []


class GatewayHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        target_backend = next(backend_pool)
        full_url = target_backend + self.path
        try:
            req = urllib.request.Request(
                full_url, headers={"User-Agent": "Enterprise-Gateway/1.0"}
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header(
                    "Content-Type",
                    resp.headers.get("Content-Type", "application/json"),
                )
                self.send_header("X-Handled-By", target_backend)
                self.end_headers()
                self.wfile.write(data)
                log_event(
                    f"[200 OK] Forwarded {self.path} -> {target_backend}"
                )
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(
                b'{"error": "Bad Gateway: Upstream node unreachable"}'
            )
            log_event(f"[502 BAD GATEWAY] Failed contacting {target_backend}")


def log_event(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def start_gateway():
    server = socketserver.ThreadingTCPServer(
        ("127.0.0.1", 8080), GatewayHandler
    )
    status_lbl.config(
        text="Gateway LIVE at http://127.0.0.1:8080 (Round-Robin)",
        fg="#15803d",
    )
    btn_start.config(state="disabled")
    threading.Thread(target=server.serve_forever, daemon=True).start()


root = tk.Tk()
root.title("API Gateway & Load Balancer")
root.geometry("560x380")
tk.Label(
    root,
    text="API GATEWAY & LOAD BALANCER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
status_lbl = tk.Label(
    root, text="Gateway Inactive", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
btn_start = tk.Button(
    root,
    text="Start Gateway (Port 8080)",
    command=start_gateway,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
)
btn_start.pack(pady=8)
log_box = tk.Text(
    root, height=11, width=60, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=8)
root.mainloop()
