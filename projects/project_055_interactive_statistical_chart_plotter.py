# Project 55: Interactive Statistical Chart Plotter
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk


class ChartPlotter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Statistical Canvas Chart Plotter")
        self.geometry("680x480")
        self.data_points = [45, 78, 32, 95, 62, 88, 54, 110, 75]
        self.labels = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
        ]
        self.chart_type = "Bar"
        # Controls
        ctrl_bar = tk.Frame(self, pady=8, bg="#f8fafc")
        ctrl_bar.pack(fill="x")
        tk.Label(
            ctrl_bar,
            text="Select Graph Type:",
            bg="#f8fafc",
            font=("Arial", 10, "bold"),
        ).pack(side="left", padx=(20, 6))
        tk.Button(
            ctrl_bar,
            text="Bar Chart",
            command=lambda: self.set_chart("Bar"),
            bg="#2563eb",
            fg="white",
            font=("Arial", 9, "bold"),
        ).pack(side="left", padx=4)
        tk.Button(
            ctrl_bar,
            text="Line Trend",
            command=lambda: self.set_chart("Line"),
            bg="#0284c7",
            fg="white",
            font=("Arial", 9, "bold"),
        ).pack(side="left", padx=4)
        self.canvas = tk.Canvas(self, bg="#ffffff")
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)
        self.draw_chart()

    def set_chart(self, ctype):
        self.chart_type = ctype
        self.draw_chart()

    def draw_chart(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 640
        h = self.canvas.winfo_height() or 380
        # Margins
        pad_x = 60
        pad_y = 50
        graph_w = w - 2 * pad_x
        graph_h = h - 2 * pad_y
        # Draw axes
        self.canvas.create_line(
            pad_x, h - pad_y, w - pad_x, h - pad_y, width=2
        )
        self.canvas.create_line(pad_x, pad_y, pad_x, h - pad_y, width=2)
        max_val = max(self.data_points)
        step_x = graph_w / len(self.data_points)
        points = []
        for i, val in enumerate(self.data_points):
            scaled_h = (val / max_val) * (graph_h - 20)
            x = pad_x + i * step_x + (step_x / 2)
            y = (h - pad_y) - scaled_h
            points.append((x, y))
            # Label on X axis
            self.canvas.create_text(
                x, h - pad_y + 15, text=self.labels[i], font=("Arial", 9)
            )
            if self.chart_type == "Bar":
                bar_w = step_x * 0.6
                x0 = x - (bar_w / 2)
                x1 = x + (bar_w / 2)
                y0 = y
                y1 = h - pad_y
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill="#3b82f6", outline="#1d4ed8"
                )
                self.canvas.create_text(
                    x,
                    y0 - 10,
                    text=str(val),
                    font=("Arial", 8, "bold"),
                    fill="#1e3a8a",
                )
        if self.chart_type == "Line":
            for i in range(len(points) - 1):
                self.canvas.create_line(
                    points[i][0],
                    points[i][1],
                    points[i + 1][0],
                    points[i + 1][1],
                    width=3,
                    fill="#0284c7",
                )
            for x, y in points:
                self.canvas.create_oval(
                    x - 4,
                    y - 4,
                    x + 4,
                    y + 4,
                    fill="#1e3a8a",
                    outline="white",
                    width=2,
                )
                val = self.data_points[points.index((x, y))]
                self.canvas.create_text(
                    x,
                    y - 12,
                    text=str(val),
                    font=("Arial", 8, "bold"),
                    fill="#0f172a",
                )


if __name__ == "__main__":
    app = ChartPlotter()
    app.mainloop()
