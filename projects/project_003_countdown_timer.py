# Project 3: Countdown Timer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Countdown Timer")
root.geometry("400x320")
remaining = 0
running = False
display = tk.Label(root, text="00:00", font=("Arial", 40, "bold"))
display.pack(pady=25)
time_entry = tk.Entry(root, width=20, justify="center")
time_entry.pack(pady=5)
time_entry.insert(0, "60")


def update_display():
    minutes = remaining // 60
    seconds = remaining % 60
    display.config(text=f"{minutes:02d}:{seconds:02d}")


def countdown():
    global remaining, running
    if running and remaining > 0:
        remaining -= 1
        update_display()
        root.after(1000, countdown)
    elif running and remaining == 0:
        running = False
        messagebox.showinfo("Finished", "Countdown completed!")


def start_timer():
    global remaining, running
    try:
        remaining = int(time_entry.get())
        if remaining <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Input", "Enter a positive number of seconds."
        )
        return
    running = True
    update_display()
    countdown()


def pause_timer():
    global running
    running = False


def reset_timer():
    global remaining, running
    running = False
    remaining = 0
    update_display()


btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)
tk.Button(btn_frame, text="Start", command=start_timer, width=8).pack(
    side="left", padx=8
)
tk.Button(btn_frame, text="Pause", command=pause_timer, width=8).pack(
    side="left", padx=8
)
tk.Button(btn_frame, text="Reset", command=reset_timer, width=8).pack(
    side="left", padx=8
)
root.mainloop()
