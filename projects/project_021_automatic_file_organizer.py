# Project 21: Automatic File Organizer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Code": [".py", ".html", ".css", ".js", ".json", ".cpp"],
}


def organize_folder():
    folder = folder_path.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid directory.")
        return
    moved_count = 0
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            target_category = "Others"
            for category, ext_list in EXTENSIONS.items():
                if ext in ext_list:
                    target_category = category
                    break
            target_dir = os.path.join(folder, target_category)
            os.makedirs(target_dir, exist_ok=True)
            destination = os.path.join(target_dir, filename)
            # Avoid overwriting existing files
            counter = 1
            base, extension = os.path.splitext(filename)
            while os.path.exists(destination):
                destination = os.path.join(
                    target_dir, f"{base}_{counter}{extension}"
                )
                counter += 1
            shutil.move(file_path, destination)
            moved_count += 1
    messagebox.showinfo(
        "Finished", f"Organization complete! Sorted {moved_count} files."
    )


def browse():
    chosen = filedialog.askdirectory()
    if chosen:
        folder_path.set(chosen)


root = tk.Tk()
root.title("Automatic File Organizer")
root.geometry("480x250")
tk.Label(
    root,
    text="FILE ORGANIZER AUTOMATION",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=15)
folder_path = tk.StringVar()
frame = tk.Frame(root)
frame.pack(pady=10)
tk.Entry(frame, textvariable=folder_path, width=38, font=("Arial", 10)).pack(
    side="left", padx=5
)
tk.Button(frame, text="Browse...", command=browse).pack(side="left")
tk.Button(
    root,
    text="Organize Files Now",
    command=organize_folder,
    bg="#059669",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=6,
).pack(pady=20)
root.mainloop()
