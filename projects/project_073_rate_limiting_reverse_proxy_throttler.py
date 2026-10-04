# Project 73: Rate-Limiting Reverse Proxy & Throttler
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import time
import threading
import tkinter as tk

RATE_LIMIT = 5  # Max burst tokens
REFILL_RATE = 1.0  # Tokens added per second
buckets = {}
bucket_lock = threading.Lock()


class RateLimiterHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        now = time.time()
        with bucket_lock:
            if client_ip not in buckets:
                buckets[client_ip] = {
                    "tokens": RATE_LIMIT,
                    "last_refill": now,
                }
            b = buckets[client_ip]
            elapsed = now - b["last_refill"]
            b["tokens"] = min(RATE_LIMIT, b["tokens"] + elapsed * REFILL_RATE)
            b["last_refill"] = now
            if b["tokens"] >= 1.0:
                b["tokens"] -= 1.0
                allowed = True
                remaining = int(b["tokens"])
            else:
                allowed = False
                remaining = 0
        if allowed:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-RateLimit-Remaining", str(remaining))
            self.end_headers()
            resp = {
                "status": "SUCCESS",
                "message": "Request processed successfully.",
                "remaining": remaining,
            }
            self.wfile.write(str(resp).encode("utf-8"))
        else:
            self.send_response(429)
            self.send_header("Content-Type", "application/json")
            self.send_header("Retry-After", "2")
            self.end_headers()
            resp = {
                "status": "BLOCKED",
                "error": "429 Too Many Requests. Rate limit exceeded.",
            }
            self.wfile.write(str(resp).encode("utf-8"))


def start_proxy():
    server = socketserver.TCPServer(("127.0.0.1", 8082), RateLimiterHandler)
    status_lbl.config(
        text="Rate Limiter Proxy LIVE at http://127.0.0.1:8082", fg="#15803d"
    )
    btn_start.config(state="disabled")
    threading.Thread(target=server.serve_forever, daemon=True).start()


root = tk.Tk()
root.title("API Rate Limiter Proxy")
root.geometry("500x320")
tk.Label(
    root,
    text="API RATE LIMITER & THROTTLER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=15)
status_lbl = tk.Label(
    root, text="Proxy Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=5)
btn_start = tk.Button(
    root,
    text="Start Proxy (Port 8082)",
    command=start_proxy,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
)
btn_start.pack(pady=10)
info_text = tk.Text(
    root, height=7, width=54, font=("Consolas", 9), bg="#f8fafc"
)
info_text.pack(padx=20, pady=10)
info_text.insert(
    tk.END,
    "Throttling Policy:\n"
    "- Token Bucket capacity: 5 requests max\n"
    "- Refill Rate: 1 token / second\n"
    "- Excessive requests return HTTP 429 Too Many Requests\n"
    "- Test via browser or curl: http://127.0.0.1:8082\n",
)
info_text.config(state="disabled")
root.mainloop()
