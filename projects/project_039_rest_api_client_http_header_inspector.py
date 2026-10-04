# Project 39: REST API Client & HTTP Header Inspector
# 100 Real-World Python Projects - Anuj Kumar Saxena
import urllib.request
import urllib.parse
import json
import tkinter as tk
from tkinter import ttk, messagebox


def send_request():
    url = url_entry.get().strip()
    method = method_combo.get()
    raw_payload = payload_text.get("1.0", tk.END).strip()
    if not url.startswith(("http://", "https://")):
        messagebox.showerror(
            "Error", "Enter a valid URL starting with http:// or https://"
        )
        return
    resp_text.delete("1.0", tk.END)
    headers_text.delete("1.0", tk.END)
    status_lbl.config(text="Sending request...", fg="#0284c7")
    try:
        data = None
        headers = {"User-Agent": "Python-REST-Client/1.0"}
        if method == "POST" and raw_payload:
            headers["Content-Type"] = "application/json"
            data = raw_payload.encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers=headers, method=method
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            status_code = resp.status
            headers_dict = dict(resp.getheaders())
            body = resp.read().decode("utf-8", errors="ignore")
            # Try formatting JSON
            try:
                formatted_body = json.dumps(json.loads(body), indent=4)
            except:
                formatted_body = body
            status_lbl.config(text=f"Status: {status_code} OK", fg="#15803d")
            resp_text.insert(tk.END, formatted_body)
            for k, v in headers_dict.items():
                headers_text.insert(tk.END, f"{k}: {v}\n")
    except urllib.error.HTTPError as e:
        status_lbl.config(text=f"Status: {e.code} Error", fg="#dc2626")
        resp_text.insert(tk.END, e.read().decode("utf-8", errors="ignore"))
    except Exception as e:
        status_lbl.config(text="Request Failed", fg="#dc2626")
        resp_text.insert(tk.END, f"Error: {e}")


root = tk.Tk()
root.title("REST API Client & Header Inspector")
root.geometry("640x520")
tk.Label(
    root, text="REST API CLIENT", font=("Arial", 16, "bold"), fg="#0369a1"
).pack(pady=10)
top_f = tk.Frame(root)
top_f.pack(pady=5)
method_combo = ttk.Combobox(
    top_f, values=["GET", "POST"], width=6, state="readonly"
)
method_combo.pack(side="left", padx=4)
method_combo.set("GET")
url_entry = tk.Entry(top_f, width=48, font=("Arial", 10))
url_entry.pack(side="left", padx=4)
url_entry.insert(0, "https://jsonplaceholder.typicode.com/posts/1")
tk.Button(
    top_f,
    text="Send",
    command=send_request,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
).pack(side="left", padx=4)
status_lbl = tk.Label(
    root, text="Ready", font=("Arial", 11, "bold"), fg="#64748b"
)
status_lbl.pack(pady=4)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=15, pady=8)
tab_resp = ttk.Frame(notebook)
tab_payload = ttk.Frame(notebook)
tab_headers = ttk.Frame(notebook)
notebook.add(tab_resp, text="Response Body")
notebook.add(tab_payload, text="Request Payload (JSON)")
notebook.add(tab_headers, text="Response Headers")
resp_text = tk.Text(tab_resp, wrap="word", font=("Consolas", 9), bg="#f8fafc")
resp_text.pack(fill="both", expand=True)
payload_text = tk.Text(tab_payload, wrap="word", font=("Consolas", 9))
payload_text.pack(fill="both", expand=True)
payload_text.insert(
    tk.END, '{\n    "title": "foo",\n    "body": "bar",\n    "userId": 1\n}'
)
headers_text = tk.Text(
    tab_headers, wrap="word", font=("Consolas", 9), bg="#f8fafc"
)
headers_text.pack(fill="both", expand=True)
root.mainloop()
