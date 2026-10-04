# Project 37: Email Validator & MX Domain Inspector
# 100 Real-World Python Projects - Anuj Kumar Saxena
import socket
import re
import tkinter as tk
from tkinter import messagebox

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def verify_email():
    email = email_entry.get().strip()
    result_box.delete("1.0", tk.END)
    if not email:
        messagebox.showwarning("Warning", "Please enter an email address.")
        return
    # Step 1: Syntax check via Regex
    if not re.match(EMAIL_REGEX, email):
        result_box.insert(
            tk.END, "[FAIL] Syntax Check: Invalid email format!\n"
        )
        status_lbl.config(text="Invalid Format", fg="#dc2626")
        return
    else:
        result_box.insert(
            tk.END, "[PASS] Syntax Check: Format conforms to standard.\n"
        )
    # Step 2: Domain extraction
    domain = email.split("@")[1]
    result_box.insert(tk.END, f"[INFO] Domain Target: {domain}\n")
    # Step 3: DNS Host Resolution via Socket
    try:
        ip = socket.gethostbyname(domain)
        result_box.insert(
            tk.END, f"[PASS] DNS Resolution: Domain active at IP: {ip}\n"
        )
        # Check standard mail server port reachability (Port 25 or 587)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        port_test = s.connect_ex((domain, 25))
        s.close()
        if port_test == 0:
            result_box.insert(
                tk.END,
                "[PASS] Mail Server: SMTP Port 25 accepts connections.\n",
            )
        else:
            result_box.insert(
                tk.END,
                "[INFO] Mail Server: Active domain (SMTP Port 25 filtered or firewalled).\n",
            )
        status_lbl.config(text="Email Domain Verified & Valid", fg="#15803d")
    except socket.gaierror:
        result_box.insert(
            tk.END,
            f"[FAIL] DNS Resolution: Domain '{domain}' does not exist!\n",
        )
        status_lbl.config(text="Domain Does Not Exist", fg="#dc2626")
    except Exception as e:
        result_box.insert(tk.END, f"[ERROR] Verification failed: {e}\n")
        status_lbl.config(text="Verification Error", fg="#dc2626")


root = tk.Tk()
root.title("Email & Domain Validator")
root.geometry("480x380")
tk.Label(
    root,
    text="EMAIL & DOMAIN VALIDATOR",
    font=("Arial", 16, "bold"),
    fg="#0369a1",
).pack(pady=15)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="Email Address:").pack(side="left", padx=4)
email_entry = tk.Entry(f, width=28, font=("Arial", 10))
email_entry.pack(side="left", padx=4)
email_entry.insert(0, "test@gmail.com")
tk.Button(
    f,
    text="Verify",
    command=verify_email,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
).pack(side="left")
status_lbl = tk.Label(
    root,
    text="Enter an email to test",
    font=("Arial", 11, "bold"),
    fg="#64748b",
)
status_lbl.pack(pady=8)
result_box = tk.Text(
    root, height=10, width=54, font=("Consolas", 9), bg="#f8fafc"
)
result_box.pack(padx=20, pady=10)
root.bind("<Return>", lambda e: verify_email())
root.mainloop()
