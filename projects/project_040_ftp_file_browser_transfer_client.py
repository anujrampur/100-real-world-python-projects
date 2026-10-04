# Project 40: FTP File Browser & Transfer Client
# 100 Real-World Python Projects - Anuj Kumar Saxena
import ftplib
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

ftp = None


def connect_ftp():
    global ftp
    host = host_entry.get().strip()
    user = user_entry.get().strip() or "anonymous"
    pwd = pwd_entry.get().strip() or "anonymous@"
    if not host:
        messagebox.showerror("Error", "Enter FTP host.")
        return
    try:
        ftp = ftplib.FTP(host, timeout=10)
        ftp.login(user=user, passwd=pwd)
        status_lbl.config(text=f"Connected to {host}", fg="#15803d")
        btn_connect.config(state="disabled")
        load_files()
    except Exception as e:
        messagebox.showerror("FTP Error", f"Connection failed: {e}")


def load_files():
    if not ftp:
        return
    file_listbox.delete(0, tk.END)
    try:
        lines = []
        ftp.dir(lines.append)
        for line in lines:
            file_listbox.insert(tk.END, line)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list directory: {e}")


def download_file():
    sel = file_listbox.curselection()
    if not sel or not ftp:
        messagebox.showwarning("Select", "Select a file to download.")
        return
    line = file_listbox.get(sel[0])
    filename = line.split()[-1]
    save_path = filedialog.asksaveasfilename(initialfile=filename)
    if not save_path:
        return

    def run():
        try:
            with open(save_path, "wb") as f:
                ftp.retrbinary(f"RETR {filename}", f.write)
            messagebox.showinfo(
                "Success", f"Downloaded {filename} successfully!"
            )
        except Exception as e:
            messagebox.showerror("Download Error", f"{e}")

    threading.Thread(target=run, daemon=True).start()


root = tk.Tk()
root.title("FTP File Explorer")
root.geometry("560x480")
tk.Label(
    root,
    text="FTP FILE BROWSER & CLIENT",
    font=("Arial", 16, "bold"),
    fg="#0369a1",
).pack(pady=10)
conn_f = tk.Frame(root)
conn_f.pack(pady=5)
tk.Label(conn_f, text="Host:").grid(row=0, column=0, padx=2)
host_entry = tk.Entry(conn_f, width=18)
host_entry.grid(row=0, column=1, padx=4)
host_entry.insert(0, "test.rebex.net")
tk.Label(conn_f, text="User:").grid(row=0, column=2, padx=2)
user_entry = tk.Entry(conn_f, width=10)
user_entry.grid(row=0, column=3, padx=4)
user_entry.insert(0, "demo")
tk.Label(conn_f, text="Pass:").grid(row=0, column=4, padx=2)
pwd_entry = tk.Entry(conn_f, width=10, show="*")
pwd_entry.grid(row=0, column=5, padx=4)
pwd_entry.insert(0, "password")
btn_connect = tk.Button(
    root,
    text="Connect to Server",
    command=connect_ftp,
    bg="#0284c7",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
)
btn_connect.pack(pady=6)
status_lbl = tk.Label(
    root, text="Not connected", font=("Arial", 10), fg="#64748b"
)
status_lbl.pack()
file_listbox = tk.Listbox(root, width=64, height=14, font=("Consolas", 9))
file_listbox.pack(padx=20, pady=10)
tk.Button(
    root,
    text="Download Selected File",
    command=download_file,
    bg="#15803d",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
).pack(pady=5)
root.mainloop()
