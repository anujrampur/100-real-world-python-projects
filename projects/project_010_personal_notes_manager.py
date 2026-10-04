# Project 10: Personal Notes Manager
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "notes.json"


def load_notes():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_notes():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(notes, f, indent=4, ensure_ascii=False)
        return True
    except OSError:
        messagebox.showerror("Save Error", "Unable to save notes to disk.")
        return False


def refresh_list():
    notes_list.delete(0, tk.END)
    for note in notes:
        notes_list.insert(tk.END, note["title"])


def new_note():
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    notes_list.selection_clear(0, tk.END)


def create_note():
    title = title_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()
    if not title:
        messagebox.showwarning("Title Required", "Enter a note title.")
        return
    notes.append({"title": title, "content": content})
    if save_notes():
        refresh_list()
        new_note()


def open_note(event=None):
    selection = notes_list.curselection()
    if not selection:
        return
    note = notes[selection[0]]
    title_entry.delete(0, tk.END)
    title_entry.insert(0, note["title"])
    content_text.delete("1.0", tk.END)
    content_text.insert("1.0", note["content"])


def update_note():
    selection = notes_list.curselection()
    if not selection:
        messagebox.showwarning(
            "No Selection", "Select a note from the list first."
        )
        return
    title = title_entry.get().strip()
    content = content_text.get("1.0", tk.END).strip()
    if not title:
        messagebox.showwarning("Title Required", "Enter a note title.")
        return
    notes[selection[0]] = {"title": title, "content": content}
    if save_notes():
        refresh_list()


def delete_note():
    selection = notes_list.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a note to delete.")
        return
    if messagebox.askyesno(
        "Confirm Delete", "Are you sure you want to delete this note?"
    ):
        notes.pop(selection[0])
        if save_notes():
            refresh_list()
            new_note()


notes = load_notes()
root = tk.Tk()
root.title("Personal Notes Manager")
root.geometry("700x480")
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=15, pady=10)
# Sidebar
left = tk.Frame(main_frame)
left.pack(side="left", fill="y", padx=(0, 15))
tk.Label(left, text="Saved Notes", font=("Arial", 11, "bold")).pack(pady=4)
notes_list = tk.Listbox(left, width=22, height=20)
notes_list.pack(fill="both", expand=True)
notes_list.bind("<<ListboxSelect>>", open_note)
# Note editor
right = tk.Frame(main_frame)
right.pack(side="right", fill="both", expand=True)
tk.Label(right, text="Title:").pack(anchor="w")
title_entry = tk.Entry(right, font=("Arial", 11))
title_entry.pack(fill="x", pady=(2, 8))
tk.Label(right, text="Content:").pack(anchor="w")
content_text = tk.Text(right, wrap="word", height=14)
content_text.pack(fill="both", expand=True)
btn_frame = tk.Frame(right)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="New", command=new_note, width=8).pack(
    side="left", padx=4
)
tk.Button(
    btn_frame,
    text="Save New",
    command=create_note,
    width=10,
    bg="#2563eb",
    fg="white",
).pack(side="left", padx=4)
tk.Button(btn_frame, text="Update", command=update_note, width=8).pack(
    side="left", padx=4
)
tk.Button(
    btn_frame, text="Delete", command=delete_note, width=8, fg="#c53030"
).pack(side="left", padx=4)
refresh_list()
root.mainloop()
