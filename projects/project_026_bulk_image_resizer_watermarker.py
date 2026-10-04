# Project 26: Bulk Image Resizer & Watermarker
# 100 Real-World Python Projects - Anuj Kumar Saxena
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# 5x7 pixel font for the watermark (rows are bit patterns, MSB = left pixel)
FONT = {
    "A": [14, 17, 17, 31, 17, 17, 17],
    "B": [30, 17, 17, 30, 17, 17, 30],
    "C": [14, 17, 16, 16, 16, 17, 14],
    "D": [30, 17, 17, 17, 17, 17, 30],
    "E": [31, 16, 16, 30, 16, 16, 31],
    "F": [31, 16, 16, 30, 16, 16, 16],
    "G": [14, 17, 16, 23, 17, 17, 15],
    "H": [17, 17, 17, 31, 17, 17, 17],
    "I": [14, 4, 4, 4, 4, 4, 14],
    "J": [7, 2, 2, 2, 2, 18, 12],
    "K": [17, 18, 20, 24, 20, 18, 17],
    "L": [16, 16, 16, 16, 16, 16, 31],
    "M": [17, 27, 21, 21, 17, 17, 17],
    "N": [17, 25, 21, 19, 17, 17, 17],
    "O": [14, 17, 17, 17, 17, 17, 14],
    "P": [30, 17, 17, 30, 16, 16, 16],
    "Q": [14, 17, 17, 17, 21, 18, 13],
    "R": [30, 17, 17, 30, 20, 18, 17],
    "S": [15, 16, 16, 14, 1, 1, 30],
    "T": [31, 4, 4, 4, 4, 4, 4],
    "U": [17, 17, 17, 17, 17, 17, 14],
    "V": [17, 17, 17, 17, 17, 10, 4],
    "W": [17, 17, 17, 21, 21, 27, 17],
    "X": [17, 17, 10, 4, 10, 17, 17],
    "Y": [17, 17, 10, 4, 4, 4, 4],
    "Z": [31, 1, 2, 4, 8, 16, 31],
    "0": [14, 17, 19, 21, 25, 17, 14],
    "1": [4, 12, 4, 4, 4, 4, 14],
    "2": [14, 17, 1, 2, 4, 8, 31],
    "3": [30, 1, 1, 14, 1, 1, 30],
    "4": [2, 6, 10, 18, 31, 2, 2],
    "5": [31, 16, 30, 1, 1, 17, 14],
    "6": [6, 8, 16, 30, 17, 17, 14],
    "7": [31, 1, 2, 4, 8, 8, 8],
    "8": [14, 17, 17, 14, 17, 17, 14],
    "9": [14, 17, 17, 15, 1, 2, 12],
    " ": [0, 0, 0, 0, 0, 0, 0],
    "-": [0, 0, 0, 31, 0, 0, 0],
    ".": [0, 0, 0, 0, 0, 12, 12],
    "(": [2, 4, 8, 8, 8, 4, 2],
    ")": [8, 4, 2, 2, 2, 4, 8],
    "@": [14, 17, 23, 21, 23, 16, 14],
}


def stamp_text(img, text, color="#ffffff", scale=2):
    """Draw watermark text onto a PhotoImage, bottom-right corner."""
    text = text.upper().replace("\u00a9", "(C)")
    glyphs = [FONT.get(ch, FONT[" "]) for ch in text]
    total_w = len(glyphs) * 6 * scale
    x0 = max(2, img.width() - total_w - 6)
    y0 = max(2, img.height() - 7 * scale - 6)
    for gi, rows in enumerate(glyphs):
        for ry, bits in enumerate(rows):
            for rx in range(5):
                if bits & (1 << (4 - rx)):
                    px = x0 + (gi * 6 + rx) * scale
                    py = y0 + ry * scale
                    img.put(color, to=(px, py, px + scale, py + scale))


def resize_to_width(img, target_w):
    """Integer-ratio resize using Tk's zoom/subsample (standard library only)."""
    w = img.width()
    if w <= target_w:
        return img
    factor = max(1, round(w / target_w))
    return img.subsample(factor, factor)


def process_images():
    src_dir = src_entry.get().strip()
    watermark_text = wm_entry.get().strip()
    try:
        target_w = int(width_entry.get())
        if target_w < 50:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Enter a valid target width (50 or more)."
        )
        return
    if not src_dir or not os.path.isdir(src_dir):
        messagebox.showerror("Error", "Select a valid source directory.")
        return
    out_dir = os.path.join(src_dir, "Processed_Images")
    os.makedirs(out_dir, exist_ok=True)
    supported = (".png", ".gif", ".ppm", ".pgm")
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(supported)]
    if not files:
        messagebox.showwarning(
            "No Images", "No PNG/GIF/PPM images found in folder."
        )
        return
    report = []
    for file in files:
        try:
            img = tk.PhotoImage(file=os.path.join(src_dir, file))
            old = (img.width(), img.height())
            img = resize_to_width(img, target_w)
            if watermark_text:
                stamp_text(img, watermark_text)
            name = os.path.splitext(file)[0] + "_processed.png"
            img.write(os.path.join(out_dir, name), format="png")
            report.append(
                f"OK  {file}: {old[0]}x{old[1]} -> {img.width()}x{img.height()}"
            )
        except tk.TclError as e:
            report.append(f"SKIPPED {file}: {e}")
    summary_text.delete("1.0", tk.END)
    summary_text.insert(
        tk.END, f"Processed {len(files)} image(s):\n" + "\n".join(report)
    )
    messagebox.showinfo("Done", f"Results saved in:\n{out_dir}")


def browse_dir():
    folder = filedialog.askdirectory()
    if folder:
        src_entry.delete(0, tk.END)
        src_entry.insert(0, folder)


root = tk.Tk()
root.title("Bulk Image Resizer & Watermarker")
root.geometry("520x440")
tk.Label(
    root,
    text="BULK IMAGE PROCESSOR",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=10)
f1 = tk.Frame(root)
f1.pack(pady=5)
src_entry = tk.Entry(f1, width=35)
src_entry.pack(side="left", padx=5)
tk.Button(f1, text="Browse Folder", command=browse_dir).pack(side="left")
f2 = tk.Frame(root)
f2.pack(pady=5)
tk.Label(f2, text="Watermark:").pack(side="left", padx=4)
wm_entry = tk.Entry(f2, width=22)
wm_entry.pack(side="left", padx=4)
wm_entry.insert(0, "(C) 2026 MY BRAND")
tk.Label(f2, text="Width px:").pack(side="left", padx=4)
width_entry = tk.Entry(f2, width=6)
width_entry.pack(side="left")
width_entry.insert(0, "400")
tk.Button(
    root,
    text="Start Batch Processing",
    command=process_images,
    bg="#059669",
    fg="white",
    font=("Arial", 10, "bold"),
    pady=4,
).pack(pady=10)
summary_text = tk.Text(root, height=12, width=58)
summary_text.pack(pady=10)
root.mainloop()
