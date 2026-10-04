# Project 59: World Timezone Clock HUD
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from datetime import datetime, timezone, timedelta
import math

TIMEZONES = [
    ("London (UTC)", 0),
    ("New Delhi (IST)", 5.5),
    ("Tokyo (JST)", 9),
    ("New York (EST)", -5),
]


class WorldClockHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("World Timezone Clock HUD")
        self.geometry("700x340")
        self.configure(bg="#0f172a")
        tk.Label(
            self,
            text="INTERNATIONAL WORLD CLOCK HUD",
            font=("Arial", 16, "bold"),
            fg="#38bdf8",
            bg="#0f172a",
        ).pack(pady=15)
        clocks_frame = tk.Frame(self, bg="#0f172a")
        clocks_frame.pack(fill="both", expand=True, padx=15)
        self.displays = []
        for city, offset in TIMEZONES:
            card = tk.Frame(
                clocks_frame,
                bg="#1e293b",
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
            )
            card.pack(side="left", fill="both", expand=True, padx=6)
            tk.Label(
                card,
                text=city,
                font=("Arial", 11, "bold"),
                fg="#f8fafc",
                bg="#1e293b",
            ).pack()
            canvas = tk.Canvas(
                card,
                width=100,
                height=100,
                bg="#1e293b",
                highlightthickness=0,
            )
            canvas.pack(pady=6)
            digital_lbl = tk.Label(
                card,
                text="--:--:--",
                font=("Consolas", 13, "bold"),
                fg="#38bdf8",
                bg="#1e293b",
            )
            digital_lbl.pack()
            date_lbl = tk.Label(
                card,
                text="--/--/----",
                font=("Arial", 8),
                fg="#94a3b8",
                bg="#1e293b",
            )
            date_lbl.pack()
            self.displays.append((canvas, digital_lbl, date_lbl, offset))
        self.update_clocks()

    def update_clocks(self):
        now_utc = datetime.now(timezone.utc)
        for canvas, digi, date_w, offset in self.displays:
            tz = timezone(timedelta(hours=offset))
            local_dt = now_utc.astimezone(tz)
            # Update digital text
            digi.config(text=local_dt.strftime("%H:%M:%S"))
            date_w.config(text=local_dt.strftime("%a, %d %b %Y"))
            # Draw analog dial
            canvas.delete("all")
            cx, cy, r = 50, 50, 42
            canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r, outline="#475569", width=2
            )
            # Hour hand
            h_angle = math.radians(
                (local_dt.hour % 12 + local_dt.minute / 60) * 30 - 90
            )
            canvas.create_line(
                cx,
                cy,
                cx + 22 * math.cos(h_angle),
                cy + 22 * math.sin(h_angle),
                fill="#f8fafc",
                width=3,
            )
            # Minute hand
            m_angle = math.radians(local_dt.minute * 6 - 90)
            canvas.create_line(
                cx,
                cy,
                cx + 32 * math.cos(m_angle),
                cy + 32 * math.sin(m_angle),
                fill="#38bdf8",
                width=2,
            )
            # Center pin
            canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill="#f8fafc")
        self.after(1000, self.update_clocks)


if __name__ == "__main__":
    app = WorldClockHUD()
    app.mainloop()
