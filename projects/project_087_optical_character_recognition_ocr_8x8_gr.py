# Project 87: Optical Character Recognition (OCR) 8x8 Grid Matcher
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk

GRID_SIZE = 8
# 8x8 Bitmap template for Digit '1' and Digit '0'
TEMPLATES = {
    "1": [
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
    ],
    "0": [
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
    ],
}


class OCRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8x8 Matrix OCR Recognizer")
        self.geometry("440x440")
        self.grid_data = [0] * (GRID_SIZE * GRID_SIZE)
        self.buttons = []
        tk.Label(
            self,
            text="8x8 PIXEL OCR MATCHER",
            font=("Arial", 15, "bold"),
            fg="#1e3a8a",
        ).pack(pady=10)
        tk.Label(
            self,
            text="Click squares to toggle pixels, then recognize:",
            font=("Arial", 9),
        ).pack()
        grid_f = tk.Frame(self)
        grid_f.pack(pady=10)
        for i in range(GRID_SIZE * GRID_SIZE):
            r, c = divmod(i, GRID_SIZE)
            btn = tk.Button(
                grid_f,
                width=2,
                height=1,
                bg="#f8fafc",
                relief="solid",
                bd=1,
                command=lambda idx=i: self.toggle_pixel(idx),
            )
            btn.grid(row=r, column=c, padx=1, pady=1)
            self.buttons.append(btn)
        btn_f = tk.Frame(self)
        btn_f.pack(pady=6)
        tk.Button(
            btn_f,
            text="Recognize Digit",
            command=self.recognize,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        ).pack(side="left", padx=4)
        tk.Button(
            btn_f, text="Clear Grid", command=self.clear_grid, padx=8
        ).pack(side="left", padx=4)
        self.res_lbl = tk.Label(
            self,
            text="Matched Digit: --",
            font=("Arial", 12, "bold"),
            fg="#15803d",
        )
        self.res_lbl.pack(pady=6)

    def toggle_pixel(self, idx):
        self.grid_data[idx] = 1 if self.grid_data[idx] == 0 else 0
        self.buttons[idx].config(
            bg="#0f172a" if self.grid_data[idx] == 1 else "#f8fafc"
        )

    def clear_grid(self):
        self.grid_data = [0] * (GRID_SIZE * GRID_SIZE)
        for b in self.buttons:
            b.config(bg="#f8fafc")
        self.res_lbl.config(text="Matched Digit: --")

    def recognize(self):
        best_match = None
        min_distance = 65
        for digit, template in TEMPLATES.items():
            # Calculate Hamming distance (number of mismatched bits)
            dist = sum(a ^ b for a, b in zip(self.grid_data, template))
            if dist < min_distance:
                min_distance = dist
                best_match = digit
        accuracy = int(((64 - min_distance) / 64) * 100)
        self.res_lbl.config(
            text=f"Matched Digit: '{best_match}' ({accuracy}% similarity)"
        )


if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
