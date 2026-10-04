# Project 97: Full-Stack Web CMS & Dynamic Content Renderer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import http.server
import socketserver
import sqlite3
import threading
import tkinter as tk
from tkinter import messagebox

DB_NAME = "cms_site.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            slug TEXT PRIMARY KEY,
            title TEXT,
            body TEXT
        )
    """)
    c.execute(
        "INSERT OR IGNORE INTO pages VALUES ('home', 'Welcome to Python CMS', 'This is a lightweight dynamic Content Management System running on pure standard library.')"
    )
    c.execute(
        "INSERT OR IGNORE INTO pages VALUES ('about', 'About Us', 'Built by software developers who value clean, zero-dependency architectures.')"
    )
    conn.commit()
    conn.close()


HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head><title>{title}</title><style>
  body {{ font-family: Arial, sans-serif; margin: 40px auto; max-width: 650px; line-height: 1.6; 
padding: 0 10px; color: #333; }}
  nav a {{ margin-right: 15px; color: #2563eb; text-decoration: none; font-weight: bold; }}
  h1 {{ color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
</style></head>
<body>
  <nav><a href="/home">Home</a><a href="/about">About</a></nav>
  <h1>{title}</h1>
  <p>{body}</p>
</body></html>"""


class CMSHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        slug = self.path.strip("/").lower() or "home"
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT title, body FROM pages WHERE slug = ?", (slug,))
        row = c.fetchone()
        conn.close()
        if row:
            title, body = row
            rendered = HTML_TEMPLATE.format(title=title, body=body)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(rendered.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<h1>404 Page Not Found</h1>")


def start_cms():
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8086), CMSHandler)
    status_lbl.config(
        text="CMS LIVE at http://127.0.0.1:8086/home", fg="#15803d"
    )
    btn_start.config(state="disabled")
    threading.Thread(target=server.serve_forever, daemon=True).start()


init_db()
root = tk.Tk()
root.title("Dynamic Content Management System (CMS)")
root.geometry("540x360")
tk.Label(
    root,
    text="HEADLESS WEB CMS ENGINE",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
status_lbl = tk.Label(
    root, text="Server Stopped", font=("Arial", 10, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
btn_start = tk.Button(
    root,
    text="Start CMS Web Server (Port 8086)",
    command=start_cms,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=5,
)
btn_start.pack(pady=10)
info_text = tk.Text(
    root, height=8, width=58, font=("Consolas", 9), bg="#f8fafc"
)
info_text.pack(padx=20, pady=8)
info_text.insert(
    tk.END,
    "CMS Features:\n"
    "- SQLite Content Storage\n"
    "- Dynamic Slug Routing (e.g. /home, /about)\n"
    "- Clean HTML / CSS Template Rendering\n"
    "- Instant In-Memory Updates\n",
)
info_text.config(state="disabled")
root.mainloop()
