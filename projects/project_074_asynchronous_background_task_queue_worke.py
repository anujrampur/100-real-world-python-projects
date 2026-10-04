# Project 74: Asynchronous Background Task Queue & Worker
# 100 Real-World Python Projects - Anuj Kumar Saxena
import queue
import threading
import uuid
import time
import tkinter as tk
from tkinter import ttk, messagebox

task_queue = queue.Queue()
tasks_db = {}
db_lock = threading.Lock()


def worker():
    while True:
        task_id, duration = task_queue.get()
        with db_lock:
            tasks_db[task_id]["status"] = "RUNNING"
            tasks_db[task_id]["start_time"] = time.strftime("%H:%M:%S")
        # Simulate heavy compute/IO task
        time.sleep(duration)
        with db_lock:
            tasks_db[task_id]["status"] = "COMPLETED"
            tasks_db[task_id]["end_time"] = time.strftime("%H:%M:%S")
        task_queue.task_done()


# Start 2 background worker threads
for _ in range(2):
    threading.Thread(target=worker, daemon=True).start()


def enqueue_task():
    try:
        duration = int(duration_entry.get().strip())
        if duration <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter valid positive seconds.")
        return
    task_id = str(uuid.uuid4())[:8]
    with db_lock:
        tasks_db[task_id] = {
            "status": "QUEUED",
            "duration": f"{duration}s",
            "start_time": "--",
            "end_time": "--",
        }
    task_queue.put((task_id, duration))
    refresh_table()


def refresh_table():
    tree.delete(*tree.get_children())
    with db_lock:
        for tid, data in tasks_db.items():
            tree.insert(
                "",
                tk.END,
                values=(
                    tid,
                    data["duration"],
                    data["status"],
                    data["start_time"],
                    data["end_time"],
                ),
            )
    root.after(1000, refresh_table)


root = tk.Tk()
root.title("Async Task Queue & Worker Engine")
root.geometry("560x420")
tk.Label(
    root,
    text="ASYNC TASK QUEUE & WORKER ENGINE",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f_in = tk.Frame(root)
f_in.pack(pady=5)
tk.Label(f_in, text="Task Workload Duration (seconds):").pack(
    side="left", padx=4
)
duration_entry = tk.Entry(f_in, width=6, justify="center")
duration_entry.pack(side="left", padx=4)
duration_entry.insert(0, "4")
tk.Button(
    f_in,
    text="Enqueue Task",
    command=enqueue_task,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=6)
tree = ttk.Treeview(
    root,
    columns=("Task ID", "Workload", "Status", "Started", "Finished"),
    show="headings",
    height=10,
)
tree.heading("Task ID", text="Task ID")
tree.column("Task ID", width=80, anchor="center")
tree.heading("Workload", text="Duration")
tree.column("Workload", width=70, anchor="center")
tree.heading("Status", text="Status")
tree.column("Status", width=90, anchor="center")
tree.heading("Started", text="Started")
tree.column("Started", width=80, anchor="center")
tree.heading("Finished", text="Finished")
tree.column("Finished", width=80, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=10)
refresh_table()
root.mainloop()
