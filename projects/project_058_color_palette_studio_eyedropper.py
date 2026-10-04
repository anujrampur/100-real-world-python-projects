# Project 58: Color Palette Studio & Eyedropper
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import colorchooser, messagebox
import colorsys


class ColorStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color Palette Studio")
        self.geometry("540x440")
        self.current_hex = "#2563eb"
        tk.Label(
            self,
            text="COLOR PALETTE STUDIO",
            font=("Arial", 16, "bold"),
            fg="#1e3a8a",
        ).pack(pady=12)
        # Active Color Banner
        self.preview_box = tk.Label(
            self,
            text=self.current_hex,
            font=("Arial", 14, "bold"),
            fg="white",
            bg=self.current_hex,
            height=3,
        )
        self.preview_box.pack(fill="x", padx=30, pady=6)
        btn_bar = tk.Frame(self)
        btn_bar.pack(pady=8)
        tk.Button(
            btn_bar,
            text="Pick Custom Color",
            command=self.pick_color,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        ).pack(side="left", padx=5)
        tk.Button(
            btn_bar, text="Copy Hex", command=self.copy_hex, padx=10
        ).pack(side="left", padx=5)
        tk.Label(
            self,
            text="Harmonic Palette Swatches (Click swatch to copy):",
            font=("Arial", 10, "bold"),
        ).pack(pady=(12, 4))
        self.swatch_frame = tk.Frame(self)
        self.swatch_frame.pack(fill="x", padx=30, pady=5)
        self.generate_palette()

    def pick_color(self):
        col = colorchooser.askcolor(self.current_hex)[1]
        if col:
            self.current_hex = col
            self.preview_box.config(
                bg=self.current_hex, text=self.current_hex
            )
            self.generate_palette()

    def generate_palette(self):
        for child in self.swatch_frame.winfo_children():
            child.destroy()
        r = int(self.current_hex[1:3], 16) / 255.0
        g = int(self.current_hex[3:5], 16) / 255.0
        b = int(self.current_hex[5:7], 16) / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        # Generate 5 harmony points across the hue circle
        hues = [(h + (i * 0.2)) % 1.0 for i in range(5)]
        for hue in hues:
            rgb = colorsys.hsv_to_rgb(hue, s, v)
            hex_col = "#{:02x}{:02x}{:02x}".format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )
            card = tk.Label(
                self.swatch_frame,
                text=hex_col,
                bg=hex_col,
                fg="white" if v < 0.6 else "black",
                font=("Arial", 9, "bold"),
                height=3,
                relief="groove",
            )
            card.pack(side="left", fill="both", expand=True, padx=2)
            card.bind("<Button-1>", lambda e, hx=hex_col: self.copy_val(hx))

    def copy_hex(self):
        self.copy_val(self.current_hex)

    def copy_val(self, val):
        self.clipboard_clear()
        self.clipboard_append(val)
        messagebox.showinfo("Copied", f"Copied {val} to clipboard!")


if __name__ == "__main__":
    app = ColorStudio()
    app.mainloop()
