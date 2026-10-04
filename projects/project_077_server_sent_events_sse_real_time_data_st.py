# Project 77: Server-Sent Events (SSE) Real-Time Data Streamer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import json
import http.server
import socketserver
import time
import random
import threading
import tkinter as tk

is_running = False


class SSEHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            log_msg(
                f"[CONNECTED] Client {self.client_address[0]} opened stream."
            )
            try:
                while is_running:
                    telemetry_val = random.randint(50, 100)
                    event_data = (
                        "data: "
                        + json.dumps(
                            {
                                "time": time.strftime("%H:%M:%S"),
                                "metric": telemetry_val,
                            }
                        )
                        + "\n\n"
                    )
                    self.wfile.write(event_data.encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(2)
            except (ConnectionResetError, BrokenPipeError):
                log_msg(
                    f"[DISCONNECTED] Client {self.client_address[0]} closed stream."
                )
        else:
            self.send_response(404)
            self.end_headers()


def log_msg(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)


def start_streamer():
    global is_running
    is_running = True
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8085), SSEHandler)
    status_lbl.config(
        text="SSE Stream LIVE at http://127.0.0.1:8085/events", fg="#15803d"
    )
    btn_start.config(state="disabled")
    threading.Thread(target=server.serve_forever, daemon=True).start()


root = tk.Tk()
root.title("Server-Sent Events (SSE) Streamer")
root.geometry("540x360")
tk.Label(
    root,
    text="SERVER-SENT EVENTS (SSE) STREAMER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
status_lbl = tk.Label(
    root, text="Streamer Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
btn_start = tk.Button(
    root,
    text="Start SSE Streamer (Port 8085)",
    command=start_streamer,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
)
btn_start.pack(pady=8)
log_box = tk.Text(
    root, height=10, width=58, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=8)
root.mainloop()
