# Project 53: Audio & Video Media Metadata Inspector
# 100 Real-World Python Projects - Anuj Kumar Saxena
import os
import struct
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def parse_wav(filepath):
    with open(filepath, "rb") as f:
        riff, size, ftype = struct.unpack("<4sI4s", f.read(12))
        if riff != b"RIFF" or ftype != b"WAVE":
            return None
        # Locate fmt chunk
        while chunk_header := f.read(8):
            chunk_id, chunk_size = struct.unpack("<4sI", chunk_header)
            if chunk_id == b"fmt ":
                fmt_data = f.read(chunk_size)
                (
                    audio_fmt,
                    channels,
                    sample_rate,
                    byte_rate,
                    block_align,
                    bits,
                ) = struct.unpack("<HHIIHH", fmt_data[:16])
                return {
                    "Format": "Uncompressed WAV (PCM)",
                    "Channels": "Stereo (2)" if channels == 2 else "Mono (1)",
                    "Sample Rate": f"{sample_rate:,} Hz",
                    "Bit Depth": f"{bits}-bit",
                    "Bitrate": f"{(byte_rate * 8) // 1000} kbps",
                }
            else:
                f.seek(chunk_size, 1)
    return None


def parse_png(filepath):
    with open(filepath, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            return None
        length, ctype = struct.unpack(">I4s", f.read(8))
        if ctype != b"IHDR":
            return None
        width, height, depth, color = struct.unpack(">IIBB", f.read(10))
    color_names = {
        0: "Grayscale",
        2: "RGB",
        3: "Indexed",
        4: "Gray+Alpha",
        6: "RGBA",
    }
    return {
        "Format": "PNG image",
        "Resolution": f"{width} x {height} px",
        "Bit Depth": f"{depth}-bit",
        "Colour Type": color_names.get(color, str(color)),
    }


def parse_mp3(filepath):
    info = {}
    with open(filepath, "rb") as f:
        head = f.read(10)
        if head[:3] == b"ID3":
            # ID3v2 tag size is stored as four 7-bit ("synchsafe") bytes
            size = (
                (head[6] << 21) | (head[7] << 14) | (head[8] << 7) | head[9]
            )
            info["ID3v2 Tag"] = f"version 2.{head[3]}, {size:,} bytes"
        f.seek(0, 2)
        if f.tell() >= 128:
            f.seek(-128, 2)
            tail = f.read(128)
            if tail[:3] == b"TAG":

                def field(a, b):
                    return (
                        tail[a:b].split(b"\x00")[0].decode("latin-1").strip()
                    )

                info["Title"] = field(3, 33)
                info["Artist"] = field(33, 63)
                info["Album"] = field(63, 93)
    return info or None


def inspect_media():
    path = path_entry.get().strip()
    if not path or not os.path.isfile(path):
        messagebox.showerror("Error", "Select a valid media file.")
        return
    tree.delete(*tree.get_children())
    size_mb = os.path.getsize(path) / (1024 * 1024)
    tree.insert("", tk.END, values=("File Size", f"{size_mb:.2f} MB"))
    tree.insert(
        "",
        tk.END,
        values=("File Extension", os.path.splitext(path)[1].upper()),
    )
    ext = os.path.splitext(path)[1].lower()
    parsers = {".wav": parse_wav, ".png": parse_png, ".mp3": parse_mp3}
    if ext in parsers:
        meta = parsers[ext](path)
        if meta:
            for k, v in meta.items():
                tree.insert("", tk.END, values=(k, v))
        else:
            tree.insert(
                "",
                tk.END,
                values=(
                    "Parser",
                    f"No readable {ext} header found",
                ),
            )
    else:
        tree.insert(
            "",
            tk.END,
            values=(
                "Notice",
                "Supported formats: WAV, PNG, MP3",
            ),
        )


def browse():
    chosen = filedialog.askopenfilename(
        filetypes=[
            ("Media Files", "*.wav;*.mp3;*.mp4;*.png"),
            ("All Files", "*.*"),
        ]
    )
    if chosen:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, chosen)
        inspect_media()


root = tk.Tk()
root.title("Media Metadata Inspector")
root.geometry("540x380")
tk.Label(
    root,
    text="MEDIA METADATA INSPECTOR",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=5)
path_entry = tk.Entry(f, width=40, font=("Arial", 9))
path_entry.pack(side="left", padx=4)
tk.Button(f, text="Browse Media", command=browse).pack(side="left")
tree = ttk.Treeview(
    root, columns=("Property", "Value"), show="headings", height=10
)
tree.heading("Property", text="Metadata Attribute")
tree.heading("Value", text="Value")
tree.column("Property", width=180)
tree.column("Value", width=280)
tree.pack(fill="both", expand=True, padx=20, pady=10)
root.mainloop()
