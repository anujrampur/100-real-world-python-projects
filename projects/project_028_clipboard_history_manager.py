# Project 28: Clipboard History Manager
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk

history = []
last_clip = ""


def poll_clipboard():
    global last_clip
    try:
        current = root.clipboard_get().strip()
        if current and current != last_clip:
            last_clip = current
            if current in history:
                history.remove(current)
            history.insert(0, current)
            update_list()
    except tk.TclError:
        pass
    root.after(1000, poll_clipboard)


def update_list():
    query = search_entry.get().lower()
    listbox.delete(0, tk.END)
    for item in history:
        if query in item.lower():
            preview = item.replace("\n", " ")[:45]
            listbox.insert(tk.END, preview)


def restore_selected():
    sel = listbox.curselection()
    if not sel:
        return
    item = history[sel[0]]
    root.clipboard_clear()
    root.clipboard_append(item)
    status_label.config(text="Copied back to active clipboard!")


root = tk.Tk()
root.title("Clipboard History Manager")
root.geometry("450x420")
tk.Label(
    root,
    text="CLIPBOARD HISTORY MANAGER",
    font=("Arial", 15, "bold"),
    fg="#065f46",
).pack(pady=10)
search_entry = tk.Entry(root, width=35, font=("Arial", 10))
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", lambda e: update_list())
listbox = tk.Listbox(root, width=48, height=12, font=("Arial", 10))
listbox.pack(pady=10)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(
    btn_frame,
    text="Restore Selected",
    command=restore_selected,
    bg="#059669",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
).pack(side="left", padx=5)
tk.Button(
    btn_frame,
    text="Clear History",
    command=lambda: [history.clear(), update_list()],
    padx=10,
).pack(side="left", padx=5)
status_label = tk.Label(
    root,
    text="Listening for copied text...",
    font=("Arial", 9, "italic"),
    fg="#718096",
)
status_label.pack(pady=5)
poll_clipboard()
root.mainloop()
