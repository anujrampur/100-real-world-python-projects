# Project 72: Token-Based Authentication & Session Manager
# 100 Real-World Python Projects - Anuj Kumar Saxena
import hmac
import hashlib
import base64
import json
import time
import tkinter as tk
from tkinter import messagebox

SECRET_KEY = b"super-secure-production-signature-key-2026"


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def b64url_decode(s: str) -> bytes:
    padding = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode(s + padding)


def create_token(user_id: str, ttl_seconds: int = 60) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": user_id, "exp": int(time.time()) + ttl_seconds}
    hdr_b64 = b64url_encode(json.dumps(header).encode("utf-8"))
    pld_b64 = b64url_encode(json.dumps(payload).encode("utf-8"))
    signature_data = f"{hdr_b64}.{pld_b64}".encode("utf-8")
    sig = hmac.new(SECRET_KEY, signature_data, hashlib.sha256).digest()
    sig_b64 = b64url_encode(sig)
    return f"{hdr_b64}.{pld_b64}.{sig_b64}"


def verify_token(token: str):
    parts = token.strip().split(".")
    if len(parts) != 3:
        return False, "Malformed token structure!"
    hdr_b64, pld_b64, sig_b64 = parts
    signature_data = f"{hdr_b64}.{pld_b64}".encode("utf-8")
    expected_sig = hmac.new(
        SECRET_KEY, signature_data, hashlib.sha256
    ).digest()
    # Constant-time comparison prevents timing attacks
    if not hmac.compare_digest(b64url_encode(expected_sig), sig_b64):
        return False, "SIGNATURE INVALID: Token has been tampered with!"
    try:
        payload = json.loads(b64url_decode(pld_b64).decode("utf-8"))
        if time.time() > payload["exp"]:
            return False, "TOKEN EXPIRED: Session duration exceeded!"
        remaining = int(payload["exp"] - time.time())
        return (
            True,
            f"VALID! Subject: {payload['sub']} (Expires in: {remaining}s)",
        )
    except Exception as e:
        return False, f"Decode error: {e}"


def generate():
    user = user_entry.get().strip()
    if not user:
        messagebox.showwarning("Warning", "Enter a User ID.")
        return
    token = create_token(user, ttl_seconds=30)
    token_box.delete("1.0", tk.END)
    token_box.insert(tk.END, token)


def validate():
    tok = token_box.get("1.0", tk.END).strip()
    valid, msg = verify_token(tok)
    status_lbl.config(text=msg, fg="#15803d" if valid else "#dc2626")


root = tk.Tk()
root.title("Token-Based Authentication Service")
root.geometry("540x400")
tk.Label(
    root,
    text="STATELESS AUTHENTICATION & JWT ENGINE",
    font=("Arial", 14, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f1 = tk.Frame(root)
f1.pack(pady=4)
tk.Label(f1, text="User ID:").pack(side="left", padx=4)
user_entry = tk.Entry(f1, width=20)
user_entry.pack(side="left", padx=4)
user_entry.insert(0, "admin@enterprise.com")
tk.Button(
    f1,
    text="Issue Token (30s TTL)",
    command=generate,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
tk.Label(root, text="Signed Authentication Token:").pack(
    anchor="w", padx=25, pady=(8, 2)
)
token_box = tk.Text(
    root, height=5, width=58, font=("Consolas", 9), wrap="word"
)
token_box.pack(padx=25, pady=4)
tk.Button(
    root,
    text="Verify Token Signature & Expiration",
    command=validate,
    bg="#0891b2",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(pady=8)
status_lbl = tk.Label(
    root,
    text="Enter or generate token to verify",
    font=("Arial", 10, "bold"),
    fg="#64748b",
)
status_lbl.pack(pady=4)
root.mainloop()
