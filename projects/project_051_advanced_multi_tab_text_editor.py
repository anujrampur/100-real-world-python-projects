# Project 51: Advanced Multi-Tab Text Editor
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Tabbed Text Editor")
        self.geometry("750x520")
        # Menu bar
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="New Tab", command=self.new_tab, accelerator="Ctrl+N"
        )
        file_menu.add_command(
            label="Open File...", command=self.open_file, accelerator="Ctrl+O"
        )
        file_menu.add_command(
            label="Save", command=self.save_file, accelerator="Ctrl+S"
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)
        # Tabbed notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        # Status bar
        self.status_bar = tk.Label(
            self,
            text="Ready | Tabs: 0",
            bd=1,
            relief="sunken",
            anchor="w",
            font=("Arial", 9),
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.bind("<Control-n>", lambda e: self.new_tab())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.new_tab()

    def new_tab(self, content="", filename="Untitled"):
        frame = ttk.Frame(self.notebook)
        text_area = tk.Text(
            frame, wrap="word", undo=True, font=("Consolas", 11)
        )
        scroll = ttk.Scrollbar(
            frame, orient="vertical", command=text_area.yview
        )
        text_area.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        text_area.pack(fill="both", expand=True)
        text_area.insert("1.0", content)
        self.notebook.add(frame, text=filename)
        self.notebook.select(frame)
        self.update_status()

    def get_current_text(self):
        current_tab = self.notebook.select()
        if not current_tab:
            return None
        frame = self.nametowidget(current_tab)
        for child in frame.winfo_children():
            if isinstance(child, tk.Text):
                return child
        return None

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                filename = path.split("/")[-1]
                self.new_tab(content, filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        text_widget = self.get_current_text()
        if not text_widget:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("All Files", "*.*"),
            ],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text_widget.get("1.0", tk.END))
                messagebox.showinfo("Saved", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def update_status(self):
        tab_count = len(self.notebook.tabs())
        self.status_bar.config(
            text=f"Active Workspace | Open Tabs: {tab_count}"
        )


if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
