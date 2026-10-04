# Project 38: Fast File Downloader with Progress Bar
# 100 Real-World Python Projects - Anuj Kumar Saxena
import urllib.request
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

is_downloading = False


def start_download():
    global is_downloading
    url = url_entry.get().strip()
    if not url.startswith(("http://", "https://")):
        messagebox.showerror("Error", "Enter a valid download URL.")
        return
    default_filename = (
        url.split("/")[-1].split("?")[0] or "downloaded_file.bin"
    )
    save_path = filedialog.asksaveasfilename(initialfile=default_filename)
    if not save_path:
        return
    btn_download.config(state="disabled")
    is_downloading = True

    def run():
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req) as resp:
                total_size = resp.getheader("Content-Length")
                total_size = int(total_size) if total_size else 0
                downloaded = 0
                chunk_size = 64 * 1024  # 64 KB chunks
                start_time = time.perf_counter()
                with open(save_path, "wb") as f:
                    while is_downloading:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        # Calculate progress and speed
                        elapsed = max(time.perf_counter() - start_time, 0.1)
                        speed_kb = (downloaded / 1024) / elapsed
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            prog_bar["value"] = percent
                            prog_label.config(
                                text=f"{percent}% ({downloaded//(1024*1024)}MB / {total_size//(1024*1024)}MB) @ {speed_kb:.1f} KB/s"
                            )
                        else:
                            prog_label.config(
                                text=f"Downloaded {downloaded//1024} KB @ {speed_kb:.1f} KB/s"
                            )
                if is_downloading:
                    messagebox.showinfo(
                        "Success",
                        f"Download finished!\nSaved to: {save_path}",
                    )
        except Exception as e:
            messagebox.showerror("Download Error", f"{e}")
        btn_download.config(state="normal")

    threading.Thread(target=run, daemon=True).start()


root = tk.Tk()
root.title("Fast File Downloader")
root.geometry("500x320")
tk.Label(
    root,
    text="FAST FILE DOWNLOADER",
    font=("Arial", 16, "bold"),
    fg="#0369a1",
).pack(pady=15)
f = tk.Frame(root)
f.pack(pady=5)
tk.Label(f, text="File URL:").pack(anchor="w")
url_entry = tk.Entry(f, width=48, font=("Arial", 10))
url_entry.pack(pady=4)
url_entry.insert(0, "https://speed.hetzner.de/10MB.bin")
btn_download = tk.Button(
    root,
    text="Start Download",
    command=start_download,
    bg="#0284c7",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5,
)
btn_download.pack(pady=10)
prog_bar = ttk.Progressbar(
    root, orient="horizontal", length=400, mode="determinate"
)
prog_bar.pack(pady=10)
prog_label = tk.Label(root, text="Ready to download", font=("Arial", 10))
prog_label.pack()
root.mainloop()
