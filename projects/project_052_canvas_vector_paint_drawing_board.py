# Project 52: Canvas Vector Paint & Drawing Board
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import colorchooser


class PaintBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vector Paint & Drawing Board")
        self.geometry("700x520")
        self.current_color = "#1e3a8a"
        self.brush_size = 3
        self.last_x = None
        self.last_y = None
        # Control panel
        toolbar = tk.Frame(self, bg="#f1f5f9", padx=10, pady=6)
        toolbar.pack(fill="x")
        tk.Button(
            toolbar,
            text="Choose Color",
            command=self.choose_color,
            bg="#ffffff",
            font=("Arial", 9, "bold"),
        ).pack(side="left", padx=4)
        self.color_indicator = tk.Label(
            toolbar, width=3, bg=self.current_color, relief="groove"
        )
        self.color_indicator.pack(side="left", padx=4)
        tk.Label(
            toolbar, text="Size:", bg="#f1f5f9", font=("Arial", 9, "bold")
        ).pack(side="left", padx=(10, 2))
        self.size_scale = tk.Scale(
            toolbar,
            from_=1,
            to=20,
            orient="horizontal",
            bg="#f1f5f9",
            highlightthickness=0,
        )
        self.size_scale.set(self.brush_size)
        self.size_scale.pack(side="left", padx=4)
        tk.Button(
            toolbar,
            text="Eraser",
            command=self.use_eraser,
            bg="#ffffff",
            font=("Arial", 9),
        ).pack(side="left", padx=6)
        tk.Button(
            toolbar,
            text="Clear Canvas",
            command=self.clear_canvas,
            bg="#fee2e2",
            fg="#991b1b",
            font=("Arial", 9, "bold"),
        ).pack(side="left", padx=4)
        # Drawing canvas
        self.canvas = tk.Canvas(self, bg="#ffffff", cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.start_stroke)
        self.canvas.bind("<B1-Motion>", self.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

    def choose_color(self):
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.current_color = color
            self.color_indicator.config(bg=self.current_color)

    def use_eraser(self):
        self.current_color = "#ffffff"
        self.color_indicator.config(bg="#ffffff")

    def clear_canvas(self):
        self.canvas.delete("all")

    def start_stroke(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw_stroke(self, event):
        size = self.size_scale.get()
        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=size,
                fill=self.current_color,
                capstyle="round",
                smooth=True,
            )
        self.last_x = event.x
        self.last_y = event.y

    def end_stroke(self, event):
        self.last_x = None
        self.last_y = None


if __name__ == "__main__":
    app = PaintBoard()
    app.mainloop()
