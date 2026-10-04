# Project 50: Two-Factor Authentication (TOTP) Authenticator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import hmac
import hashlib
import time
import struct
import base64
import tkinter as tk
from tkinter import messagebox


def get_totp_code(secret_b32: str, interval: int = 30) -> str:
    # Normalize secret
    key = base64.b32decode(secret_b32.strip().upper(), casefold=True)
    # Calculate intervals since UNIX epoch
    counter = int(time.time()) // interval
    # HMAC-SHA1
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    # Dynamic Truncation
    offset = h[-1] & 0x0F
    code = (
        struct.unpack(">I", h[offset : offset + 4])[0] & 0x7FFFFFFF
    ) % 1000000
    return f"{code:06d}"


def update_totp():
    secret = secret_entry.get().strip()
    if secret:
        try:
            code = get_totp_code(secret)
            code_label.config(text=f"{code[:3]} {code[3:]}")
            remaining = 30 - (int(time.time()) % 30)
            time_label.config(text=f"Refreshes in: {remaining}s")
        except Exception:
            code_label.config(text="INVALID SECRET")
    root.after(1000, update_totp)


root = tk.Tk()
root.title("2FA TOTP Authenticator")
root.geometry("420x340")
tk.Label(
    root,
    text="2FA TOTP AUTHENTICATOR",
    font=("Arial", 16, "bold"),
    fg="#7c2d12",
).pack(pady=15)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="Base32 Secret Key:").pack(anchor="w")
secret_entry = tk.Entry(f, width=28, font=("Consolas", 11), justify="center")
secret_entry.pack(pady=4)
secret_entry.insert(
    0, "JBSWY3DPEHPK3PXP"
)  # Standard RFC test secret ("Hello!")
code_label = tk.Label(
    root, text="--- ---", font=("Arial", 36, "bold"), fg="#b45309"
)
code_label.pack(pady=15)
time_label = tk.Label(
    root, text="Refreshes in: 30s", font=("Arial", 10, "bold"), fg="#64748b"
)
time_label.pack(pady=5)
update_totp()
root.mainloop()
