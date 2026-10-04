# Project 48: Secure Multi-Pass File Shredder
# 100 Real-World Python Projects - Anuj Kumar Saxena
import os
import secrets
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def shred_file(filepath, passes=3, callback=None):
    if not os.path.isfile(filepath):
        return False
    size = os.path.getsize(filepath)
    with open(filepath, "ba+", buffering=0) as f:
        for p in range(passes):
            f.seek(0)
            # Alternate passes: zeros, ones, cryptographically random bytes
            if p == 0:
                pattern = b"\x00" * 4096
            elif p == 1:
                pattern = b"\xff" * 4096
            else:
                pattern = secrets.token_bytes(4096)
            written = 0
            while written < size:
                to_write = min(len(pattern), size - written)
                f.write(pattern[:to_write])
                written += to_write
            f.flush()
            os.fsync(f.fileno())
            if callback:
                callback(int(((p + 1) / passes) * 100))
    # Rename file to obscure original filename before removal
    folder = os.path.dirname(filepath)
    temp_name = os.path.join(folder, secrets.token_hex(8) + ".tmp")
    os.rename(filepath, temp_name)
    os.remove(temp_name)
    return True


def start_shred():
    path = path_entry.get().strip()
    if not path or not os.path.isfile(path):
        messagebox.showerror("Error", "Select a valid file to shred.")
        return
    if not messagebox.askyesno(
        "CONFIRM PERMANENT DELETION",
        f"Are you ABSOLUTELY sure?\nThis file will be completely unrecoverable:\n{path}",
    ):
        return
    prog_bar["value"] = 0
    btn_shred.config(state="disabled")

    def update_p(val):
        prog_bar["value"] = val
        root.update_idletasks()

    try:
        shred_file(path, passes=3, callback=update_p)
        messagebox.showinfo(
            "Shredded", "File successfully shredded and unlinked!"
        )
        path_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Shredding failed: {e}")
    btn_shred.config(state="normal")


root = tk.Tk()
root.title("Secure File Shredder")
root.geometry("480x280")
tk.Label(
    root,
    text="SECURE FILE SHREDDER",
    font=("Arial", 16, "bold"),
    fg="#7c2d12",
).pack(pady=15)
f = tk.Frame(root)
f.pack(pady=5)
path_entry = tk.Entry(f, width=36, font=("Arial", 10))
path_entry.pack(side="left", padx=4)
tk.Button(
    f,
    text="Browse File",
    command=lambda: path_entry.insert(0, filedialog.askopenfilename()),
).pack(side="left")
btn_shred = tk.Button(
    root,
    text="Shred & Overwrite File (3 Passes)",
    command=start_shred,
    bg="#dc2626",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=5,
)
btn_shred.pack(pady=15)
prog_bar = ttk.Progressbar(
    root, orient="horizontal", length=380, mode="determinate"
)
prog_bar.pack(pady=10)
root.mainloop()
