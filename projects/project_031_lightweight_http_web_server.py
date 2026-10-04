# Project 31: Lightweight HTTP Web Server
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import threading
import os
import tkinter as tk
from tkinter import filedialog, messagebox

httpd = None
server_thread = None
is_running = False


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default console logs


def run_server(port, folder):
    global httpd
    os.chdir(folder)
    with socketserver.TCPServer(("", port), QuietHandler) as s:
        httpd = s
        s.serve_forever()


def toggle_server():
    global httpd, server_thread, is_running
    if not is_running:
        folder = folder_entry.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid directory.")
            return
        try:
            port = int(port_entry.get().strip())
            if port < 1024 or port > 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Enter a valid port between 1024 and 65535."
            )
            return
        server_thread = threading.Thread(
            target=run_server, args=(port, folder), daemon=True
        )
        server_thread.start()
        is_running = True
        status_label.config(
            text=f"Running at: http://localhost:{port}/", fg="#15803d"
        )
        toggle_btn.config(text="Stop Server", bg="#dc2626")
    else:
        if httpd:
            httpd.shutdown()
            httpd.server_close()
        is_running = False
        status_label.config(text="Server Stopped", fg="#64748b")
        toggle_btn.config(text="Start Server", bg="#0284c7")


def browse():
    chosen = filedialog.askdirectory()
    if chosen:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, chosen)


root = tk.Tk()
root.title("Local HTTP Web Server")
root.geometry("480x320")
tk.Label(
    root, text="LOCAL HTTP SERVER", font=("Arial", 16, "bold"), fg="#0369a1"
).pack(pady=15)
f1 = tk.Frame(root)
f1.pack(pady=5)
tk.Label(f1, text="Host Directory:").pack(anchor="w")
folder_entry = tk.Entry(f1, width=38, font=("Arial", 10))
folder_entry.pack(side="left", padx=4)
folder_entry.insert(0, os.getcwd())
tk.Button(f1, text="Browse", command=browse).pack(side="left")
f2 = tk.Frame(root)
f2.pack(pady=10)
tk.Label(f2, text="Port:").pack(side="left", padx=4)
port_entry = tk.Entry(f2, width=8, justify="center")
port_entry.pack(side="left", padx=4)
port_entry.insert(0, "8080")
toggle_btn = tk.Button(
    root,
    text="Start Server",
    command=toggle_server,
    bg="#0284c7",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5,
)
toggle_btn.pack(pady=10)
status_label = tk.Label(
    root, text="Server Stopped", font=("Arial", 11, "bold"), fg="#64748b"
)
status_label.pack(pady=10)
root.mainloop()
