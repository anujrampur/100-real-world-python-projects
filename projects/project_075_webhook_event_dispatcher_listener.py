# Project 75: Webhook Event Dispatcher & Listener
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import urllib.request
import hmac
import hashlib
import json
import threading
import tkinter as tk
from tkinter import messagebox

WEBHOOK_SECRET = b"whsec_test_secret_key_123"


class WebhookListener(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        signature = self.headers.get("X-Hub-Signature-256", "")
        expected_sig = (
            "sha256="
            + hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()
        )
        if hmac.compare_digest(expected_sig, signature):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ACCEPTED"}')
            try:
                data = json.loads(body.decode("utf-8"))
                log_msg(
                    f"[VERIFIED] Event: {data.get('event')} | User: {data.get('user')}"
                )
            except:
                pass
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"INVALID_SIGNATURE"}')
            log_msg("[REJECTED] Invalid HMAC Signature!")


def log_msg(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def send_test_webhook():
    payload = json.dumps(
        {
            "event": "payment.succeeded",
            "user": "alice@example.com",
            "amount": 49.99,
        }
    ).encode("utf-8")
    sig = (
        "sha256="
        + hmac.new(WEBHOOK_SECRET, payload, hashlib.sha256).hexdigest()
    )

    def run():
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:8083/webhook",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Hub-Signature-256": sig,
                },
            )
            with urllib.request.urlopen(req) as resp:
                pass
        except Exception as e:
            log_msg(f"[CLIENT ERROR] {e}")

    threading.Thread(target=run, daemon=True).start()


def start_server():
    server = socketserver.TCPServer(("127.0.0.1", 8083), WebhookListener)
    status_lbl.config(
        text="Webhook Listener active on port 8083", fg="#15803d"
    )
    btn_start.config(state="disabled")
    threading.Thread(target=server.serve_forever, daemon=True).start()


root = tk.Tk()
root.title("Webhook Dispatcher & Receiver")
root.geometry("540x380")
tk.Label(
    root,
    text="WEBHOOK EVENT DISPATCHER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=4)
btn_start = tk.Button(
    f,
    text="Start Webhook Receiver",
    command=start_server,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
)
btn_start.pack(side="left", padx=4)
tk.Button(
    f,
    text="Simulate Outbound Webhook",
    command=send_test_webhook,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=4)
status_lbl = tk.Label(
    root, text="Receiver Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
log_box = tk.Text(
    root, height=12, width=60, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=8)
root.mainloop()
