# Project 44: SHA-256 & MD5 File Integrity Verifier
# 100 Real-World Python Projects - Anuj Kumar Saxena
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


def calculate_checksums():
    filepath = path_entry.get().strip()
    if not filepath:
        messagebox.showerror("Error", "Select a file first.")
        return
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(64 * 1024):
                md5.update(chunk)
                sha1.update(chunk)
                sha256.update(chunk)
        res_md5.delete(0, tk.END)
        res_md5.insert(0, md5.hexdigest())
        res_sha1.delete(0, tk.END)
        res_sha1.insert(0, sha1.hexdigest())
        res_sha256.delete(0, tk.END)
        res_sha256.insert(0, sha256.hexdigest())
        verify_match()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to hash file: {e}")


def verify_match():
    expected = compare_entry.get().strip().lower()
    if not expected:
        match_lbl.config(text="")
        return
    computed = [
        res_md5.get().lower(),
        res_sha1.get().lower(),
        res_sha256.get().lower(),
    ]
    if expected in computed:
        match_lbl.config(
            text="MATCH VERIFIED: File is authentic & intact!", fg="#15803d"
        )
    else:
        match_lbl.config(
            text="MISMATCH: Checksum does not match!", fg="#dc2626"
        )


def browse():
    chosen = filedialog.askopenfilename()
    if chosen:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, chosen)
        calculate_checksums()


root = tk.Tk()
root.title("File Integrity Verifier")
root.geometry("540x420")
tk.Label(
    root,
    text="CHECKSUM & INTEGRITY VERIFIER",
    font=("Arial", 15, "bold"),
    fg="#7c2d12",
).pack(pady=12)
f1 = tk.Frame(root)
f1.pack(pady=5)
path_entry = tk.Entry(f1, width=42, font=("Arial", 9))
path_entry.pack(side="left", padx=4)
tk.Button(f1, text="Browse", command=browse).pack(side="left")
# Checksums display
fields = [
    ("MD5:", res_md5 := tk.Entry(root, width=54, font=("Consolas", 9))),
    ("SHA-1:", res_sha1 := tk.Entry(root, width=54, font=("Consolas", 9))),
    (
        "SHA-256:",
        res_sha256 := tk.Entry(root, width=54, font=("Consolas", 9)),
    ),
]
for label, entry in fields:
    tk.Label(root, text=label, font=("Arial", 9, "bold")).pack(
        anchor="w", padx=25, pady=(6, 0)
    )
    entry.pack(padx=25, pady=2)
# Compare box
tk.Label(
    root, text="Compare with Vendor Checksum:", font=("Arial", 9, "bold")
).pack(anchor="w", padx=25, pady=(12, 0))
compare_entry = tk.Entry(root, width=54, font=("Consolas", 9))
compare_entry.pack(padx=25, pady=4)
compare_entry.bind("<KeyRelease>", lambda e: verify_match())
match_lbl = tk.Label(root, text="", font=("Arial", 11, "bold"))
match_lbl.pack(pady=10)
root.mainloop()
