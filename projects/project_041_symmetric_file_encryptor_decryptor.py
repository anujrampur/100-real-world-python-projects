# Project 41: Symmetric File Encryptor & Decryptor
# 100 Real-World Python Projects - Anuj Kumar Saxena
import hashlib
import hmac
import secrets
import os
import tkinter as tk
from tkinter import filedialog, messagebox

SALT_SIZE = 16
MAGIC_HEADER = b"ENC_FILE_V2"


def derive_keys(password: str, salt: bytes):
    """PBKDF2 gives 64 bytes: first 32 for the cipher stream, last 32 for the HMAC tag."""
    material = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 200000, dklen=64
    )
    return material[:32], material[32:]


def keystream(key: bytes, length: int) -> bytes:
    stream = bytearray()
    counter = 0
    while len(stream) < length:
        stream.extend(
            hashlib.sha256(key + counter.to_bytes(8, "big")).digest()
        )
        counter += 1
    return bytes(stream[:length])


def xor_bytes(data: bytes, stream: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, stream))


def encrypt_file():
    filepath = file_entry.get().strip()
    password = pwd_entry.get()
    if not filepath or not os.path.isfile(filepath) or not password:
        messagebox.showerror(
            "Error", "Select a valid file and enter a password."
        )
        return
    out_path = filepath + ".enc"
    salt = secrets.token_bytes(SALT_SIZE)
    try:
        with open(filepath, "rb") as f:
            plaintext = f.read()
        enc_key, mac_key = derive_keys(password, salt)
        ciphertext = xor_bytes(plaintext, keystream(enc_key, len(plaintext)))
        tag = hmac.new(mac_key, salt + ciphertext, hashlib.sha256).digest()
        with open(out_path, "wb") as f:
            f.write(MAGIC_HEADER + salt + tag + ciphertext)
        messagebox.showinfo(
            "Success", f"Encrypted successfully!\nSaved to:\n{out_path}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")


def decrypt_file():
    filepath = file_entry.get().strip()
    password = pwd_entry.get()
    if not filepath or not os.path.isfile(filepath) or not password:
        messagebox.showerror(
            "Error", "Select a valid encrypted file and enter a password."
        )
        return
    out_path = (
        filepath[:-4] if filepath.endswith(".enc") else filepath + ".dec"
    )
    try:
        with open(filepath, "rb") as f:
            header = f.read(len(MAGIC_HEADER))
            if header != MAGIC_HEADER:
                messagebox.showerror(
                    "Error", "Invalid file header! Not an encrypted file."
                )
                return
            salt = f.read(SALT_SIZE)
            tag = f.read(32)
            ciphertext = f.read()
        enc_key, mac_key = derive_keys(password, salt)
        expected = hmac.new(
            mac_key, salt + ciphertext, hashlib.sha256
        ).digest()
        if not hmac.compare_digest(tag, expected):
            messagebox.showerror(
                "Error",
                "Wrong password or the file was modified. Nothing was written.",
            )
            return
        decrypted = xor_bytes(ciphertext, keystream(enc_key, len(ciphertext)))
        with open(out_path, "wb") as f:
            f.write(decrypted)
        messagebox.showinfo(
            "Success", f"Decrypted successfully!\nSaved to:\n{out_path}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")


def browse():
    chosen = filedialog.askopenfilename()
    if chosen:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, chosen)


root = tk.Tk()
root.title("File Encryptor & Decryptor")
root.geometry("480x280")
tk.Label(
    root,
    text="SYMMETRIC FILE ENCRYPTOR",
    font=("Arial", 15, "bold"),
    fg="#7c2d12",
).pack(pady=15)
f1 = tk.Frame(root)
f1.pack(pady=5)
file_entry = tk.Entry(f1, width=36, font=("Arial", 10))
file_entry.pack(side="left", padx=4)
tk.Button(f1, text="Browse File", command=browse).pack(side="left")
f2 = tk.Frame(root)
f2.pack(pady=8)
tk.Label(f2, text="Secret Password:").pack(side="left", padx=4)
pwd_entry = tk.Entry(f2, width=22, show="*")
pwd_entry.pack(side="left", padx=4)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)
tk.Button(
    btn_frame,
    text="Encrypt File",
    command=encrypt_file,
    bg="#b45309",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=5,
).pack(side="left", padx=8)
tk.Button(
    btn_frame,
    text="Decrypt File",
    command=decrypt_file,
    bg="#15803d",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=5,
).pack(side="left", padx=8)
root.mainloop()
