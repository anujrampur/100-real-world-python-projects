# Project 54: Kanban Task Management Board
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

DB_FILE = "kanban_tasks.json"


class KanbanBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kanban Task Management Board")
        self.geometry("720x460")
        self.columns = {"todo": [], "in_progress": [], "done": []}
        self.load_data()
        # Title and Top Controls
        top_bar = tk.Frame(self, pady=10)
        top_bar.pack(fill="x")
        tk.Label(
            top_bar,
            text="KANBAN PRODUCTIVITY BOARD",
            font=("Arial", 16, "bold"),
            fg="#1e3a8a",
        ).pack(side="left", padx=20)
        tk.Button(
            top_bar,
            text="+ Add New Task",
            command=self.add_task,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=3,
        ).pack(side="right", padx=20)
        # Columns container
        col_frame = tk.Frame(self)
        col_frame.pack(fill="both", expand=True, padx=15, pady=5)
        self.boxes = {}
        col_configs = [
            ("todo", "TO DO", "#f8fafc", "#e2e8f0"),
            ("in_progress", "IN PROGRESS", "#f0f9ff", "#bae6fd"),
            ("done", "DONE", "#f0fdf4", "#bbf7d0"),
        ]
        for key, title, bg_col, bd_col in col_configs:
            frame = tk.Frame(
                col_frame, bg=bg_col, bd=1, relief="solid", padx=8, pady=8
            )
            frame.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(
                frame, text=title, font=("Arial", 11, "bold"), bg=bg_col
            ).pack(pady=(0, 6))
            lb = tk.Listbox(
                frame, font=("Arial", 10), bg="#ffffff", selectmode="single"
            )
            lb.pack(fill="both", expand=True)
            self.boxes[key] = lb
            btn_f = tk.Frame(frame, bg=bg_col)
            btn_f.pack(pady=6)
            if key == "todo":
                tk.Button(
                    btn_f,
                    text="Move ->",
                    command=lambda: self.move_task("todo", "in_progress"),
                ).pack(side="left", padx=2)
            elif key == "in_progress":
                tk.Button(
                    btn_f,
                    text="<- Back",
                    command=lambda: self.move_task("in_progress", "todo"),
                ).pack(side="left", padx=2)
                tk.Button(
                    btn_f,
                    text="Done ->",
                    command=lambda: self.move_task("in_progress", "done"),
                ).pack(side="left", padx=2)
            elif key == "done":
                tk.Button(
                    btn_f,
                    text="Delete",
                    command=self.delete_done,
                    fg="#dc2626",
                ).pack(side="left", padx=2)
        self.refresh_ui()

    def add_task(self):
        task = simpledialog.askstring("New Task", "Enter task description:")
        if task and task.strip():
            self.columns["todo"].append(task.strip())
            self.save_data()
            self.refresh_ui()

    def move_task(self, source, target):
        sel = self.boxes[source].curselection()
        if not sel:
            messagebox.showwarning(
                "Select Task", "Please select a task to move."
            )
            return
        task = self.columns[source].pop(sel[0])
        self.columns[target].append(task)
        self.save_data()
        self.refresh_ui()

    def delete_done(self):
        sel = self.boxes["done"].curselection()
        if not sel:
            return
        self.columns["done"].pop(sel[0])
        self.save_data()
        self.refresh_ui()

    def refresh_ui(self):
        for key in self.columns:
            self.boxes[key].delete(0, tk.END)
            for item in self.columns[key]:
                self.boxes[key].insert(tk.END, item)

    def save_data(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.columns, f, indent=4)

    def load_data(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    self.columns = json.load(f)
            except Exception:
                pass


if __name__ == "__main__":
    app = KanbanBoard()
    app.mainloop()
