# Project 42: Cryptographic Password Vault
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import hashlib
import hmac
import secrets
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "vault.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS master (
            id INTEGER PRIMARY KEY,
            salt BLOB,
            hash TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            username TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


session_key = None  # derived from the master password; lives in memory only


def hash_master(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 120000
    ).hex()


def derive_vault_key(password: str, salt: bytes) -> bytes:
    # A different iteration count + label keeps this key independent of the login hash
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), b"vault-key" + salt, 150000, dklen=32
    )


def seal(key: bytes, text: str) -> str:
    """Encrypt + authenticate one secret. Returns hex(nonce + tag + ciphertext)."""
    nonce = secrets.token_bytes(16)
    data = text.encode("utf-8")
    stream = b"".join(
        hashlib.sha256(key + nonce + i.to_bytes(4, "big")).digest()
        for i in range(len(data) // 32 + 1)
    )[: len(data)]
    cipher = bytes(a ^ b for a, b in zip(data, stream))
    tag = hmac.new(key, nonce + cipher, hashlib.sha256).digest()
    return (nonce + tag + cipher).hex()


def unseal(key: bytes, blob_hex: str) -> str:
    raw = bytes.fromhex(blob_hex)
    nonce, tag, cipher = raw[:16], raw[16:48], raw[48:]
    if not hmac.compare_digest(
        tag, hmac.new(key, nonce + cipher, hashlib.sha256).digest()
    ):
        return "[tampered entry]"
    stream = b"".join(
        hashlib.sha256(key + nonce + i.to_bytes(4, "big")).digest()
        for i in range(len(cipher) // 32 + 1)
    )[: len(cipher)]
    return bytes(a ^ b for a, b in zip(cipher, stream)).decode("utf-8")


def setup_or_login():
    global session_key
    pwd = master_entry.get().strip()
    if not pwd:
        messagebox.showerror("Error", "Enter master password.")
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT salt, hash FROM master WHERE id = 1")
    row = c.fetchone()
    if not row:
        # First-time master password setup
        salt = secrets.token_bytes(16)
        h = hash_master(pwd, salt)
        c.execute(
            "INSERT INTO master (id, salt, hash) VALUES (1, ?, ?)", (salt, h)
        )
        conn.commit()
        conn.close()
        session_key = derive_vault_key(pwd, salt)
        messagebox.showinfo(
            "Setup", "Master Password established! Vault unlocked."
        )
        unlock_vault()
    else:
        salt, stored_hash = row
        if hmac.compare_digest(hash_master(pwd, salt), stored_hash):
            conn.close()
            session_key = derive_vault_key(pwd, salt)
            unlock_vault()
        else:
            conn.close()
            messagebox.showerror("Denied", "Incorrect Master Password!")


def unlock_vault():
    auth_frame.pack_forget()
    vault_frame.pack(fill="both", expand=True, padx=15, pady=10)
    load_vault()


def add_credential():
    svc = svc_entry.get().strip()
    usr = usr_entry.get().strip()
    pwd = cred_pwd_entry.get().strip()
    if not svc or not usr or not pwd:
        messagebox.showwarning(
            "Warning", "All credential fields are required."
        )
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO credentials (service, username, password) VALUES (?, ?, ?)",
        (svc, usr, seal(session_key, pwd)),
    )
    conn.commit()
    conn.close()
    svc_entry.delete(0, tk.END)
    usr_entry.delete(0, tk.END)
    cred_pwd_entry.delete(0, tk.END)
    load_vault()


def load_vault():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT service, username, password FROM credentials")
    for service, username, blob in c.fetchall():
        tree.insert(
            "", tk.END, values=(service, username, unseal(session_key, blob))
        )
    conn.close()


init_db()
root = tk.Tk()
root.title("Cryptographic Password Vault")
root.geometry("540x480")
tk.Label(
    root,
    text="SECURE PASSWORD VAULT",
    font=("Arial", 16, "bold"),
    fg="#7c2d12",
).pack(pady=12)
# Auth Screen
auth_frame = tk.Frame(root)
auth_frame.pack(pady=40)
tk.Label(
    auth_frame, text="Enter Master Password to Unlock:", font=("Arial", 11)
).pack(pady=5)
master_entry = tk.Entry(
    auth_frame, width=24, show="*", font=("Arial", 12), justify="center"
)
master_entry.pack(pady=8)
tk.Button(
    auth_frame,
    text="Unlock Vault",
    command=setup_or_login,
    bg="#b45309",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(pady=5)
# Unlocked Vault Interface
vault_frame = tk.Frame(root)
f_in = tk.Frame(vault_frame)
f_in.pack(pady=5)
svc_entry = tk.Entry(f_in, width=12)
svc_entry.pack(side="left", padx=2)
usr_entry = tk.Entry(f_in, width=14)
usr_entry.pack(side="left", padx=2)
cred_pwd_entry = tk.Entry(f_in, width=12)
cred_pwd_entry.pack(side="left", padx=2)
tk.Button(
    f_in,
    text="Add Entry",
    command=add_credential,
    bg="#15803d",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=4)
tree = ttk.Treeview(
    vault_frame,
    columns=("Service", "Username", "Password"),
    show="headings",
    height=12,
)
tree.heading("Service", text="Service")
tree.heading("Username", text="Username / Email")
tree.heading("Password", text="Password")
tree.column("Service", width=120)
tree.column("Username", width=180)
tree.column("Password", width=140)
tree.pack(fill="both", expand=True, pady=10)
root.mainloop()
