# Project 43: Steganography Image Data Hider
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import filedialog, messagebox


def encode_lsb(data: bytes, message: str) -> bytes:
    # Append null terminator to signal end of message
    msg_bytes = message.encode("utf-8") + b"\x00"
    bits = []
    for b in msg_bytes:
        for i in range(8):
            bits.append((b >> (7 - i)) & 1)
    if len(bits) > len(data):
        raise ValueError("Message too large for cover data!")
    mutable = bytearray(data)
    for i, bit in enumerate(bits):
        mutable[i] = (mutable[i] & ~1) | bit
    return bytes(mutable)


def decode_lsb(data: bytes) -> str:
    bits = []
    chars = bytearray()
    for byte in data:
        bits.append(byte & 1)
        if len(bits) == 8:
            val = 0
            for bit in bits:
                val = (val << 1) | bit
            if val == 0:  # Reached null-terminator
                break
            chars.append(val)
            bits = []
    return chars.decode("utf-8", errors="ignore")


def bmp_pixel_offset(raw: bytes) -> int:
    """Return where pixel data starts in an uncompressed 24-bit BMP, or raise ValueError."""
    if len(raw) < 54 or raw[:2] != b"BM":
        raise ValueError(
            "Not a BMP file. Use an uncompressed 24-bit .bmp image."
        )
    offset = int.from_bytes(raw[10:14], "little")
    bits_per_pixel = int.from_bytes(raw[28:30], "little")
    compression = int.from_bytes(raw[30:34], "little")
    if bits_per_pixel != 24 or compression != 0:
        raise ValueError("Only uncompressed 24-bit BMP images are supported.")
    return offset


def hide_message():
    filepath = file_entry.get().strip()
    msg = msg_text.get("1.0", tk.END).strip()
    if not filepath or not msg:
        messagebox.showerror(
            "Error", "Select a BMP image and enter a message."
        )
        return
    out_path = (
        filepath[:-4] + "_stego.bmp"
        if filepath.lower().endswith(".bmp")
        else filepath + "_stego.bmp"
    )
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        offset = bmp_pixel_offset(raw)
        header, pixels = raw[:offset], raw[offset:]
        with open(out_path, "wb") as f:
            f.write(header + encode_lsb(pixels, msg))
        messagebox.showinfo(
            "Success", f"Secret message embedded!\nSaved to:\n{out_path}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Encoding failed: {e}")


def extract_message():
    filepath = file_entry.get().strip()
    if not filepath:
        messagebox.showerror("Error", "Select a stego BMP image.")
        return
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        offset = bmp_pixel_offset(raw)
        extracted = decode_lsb(raw[offset:])
        msg_text.delete("1.0", tk.END)
        msg_text.insert(
            tk.END, extracted if extracted else "[No hidden text detected]"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Extraction failed: {e}")


def browse():
    chosen = filedialog.askopenfilename(filetypes=[("BMP images", "*.bmp")])
    if chosen:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, chosen)


root = tk.Tk()
root.title("Steganography Text Hider")
root.geometry("480x360")
tk.Label(
    root,
    text="LSB IMAGE STEGANOGRAPHY",
    font=("Arial", 16, "bold"),
    fg="#7c2d12",
).pack(pady=12)
f1 = tk.Frame(root)
f1.pack(pady=5)
file_entry = tk.Entry(f1, width=35, font=("Arial", 10))
file_entry.pack(side="left", padx=4)
tk.Button(f1, text="Browse", command=browse).pack(side="left")
tk.Label(root, text="Secret Message Payload:").pack(pady=4)
msg_text = tk.Text(root, height=6, width=50)
msg_text.pack(pady=5)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(
    btn_frame,
    text="Hide Message",
    command=hide_message,
    bg="#b45309",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(side="left", padx=8)
tk.Button(
    btn_frame,
    text="Extract Message",
    command=extract_message,
    bg="#15803d",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(side="left", padx=8)
root.mainloop()
