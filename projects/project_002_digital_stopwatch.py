# Project 2: Digital Stopwatch
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk

root = tk.Tk()
root.title("Digital Stopwatch")
root.geometry("350x250")
running = False
elapsed_seconds = 0
display = tk.Label(root, text="00:00:00", font=("Arial", 32, "bold"))
display.pack(pady=35)


def update_timer():
    global elapsed_seconds
    if running:
        elapsed_seconds += 1
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    root.after(1000, update_timer)


def start_timer():
    global running
    running = True


def stop_timer():
    global running
    running = False


def reset_timer():
    global running, elapsed_seconds
    running = False
    elapsed_seconds = 0
    display.config(text="00:00:00")


btn_frame = tk.Frame(root)
btn_frame.pack()
tk.Button(btn_frame, text="Start", command=start_timer, width=8).pack(
    side="left", padx=10
)
tk.Button(btn_frame, text="Stop", command=stop_timer, width=8).pack(
    side="left", padx=10
)
tk.Button(btn_frame, text="Reset", command=reset_timer, width=8).pack(
    side="left", padx=10
)
update_timer()
root.mainloop()
