# Project 57: File System Tree & Search Explorer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FileExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File System Tree Explorer")
        self.geometry("640x480")
        # Search Bar
        top_bar = tk.Frame(self, pady=8)
        top_bar.pack(fill="x", padx=15)
        tk.Button(
            top_bar,
            text="Open Folder",
            command=self.browse_root,
            bg="#2563eb",
            fg="white",
            font=("Arial", 9, "bold"),
        ).pack(side="left", padx=(0, 10))
        tk.Label(top_bar, text="Filter Search:").pack(side="left", padx=4)
        self.search_entry = tk.Entry(top_bar, width=28)
        self.search_entry.pack(side="left", padx=4)
        self.search_entry.bind("<KeyRelease>", self.filter_tree)
        # Treeview
        self.tree = ttk.Treeview(
            self, columns=("Size", "Type"), show="tree headings"
        )
        self.tree.heading("#0", text="File / Directory Name", anchor="w")
        self.tree.heading("Size", text="Size (KB)")
        self.tree.heading("Type", text="Type")
        self.tree.column("#0", width=340)
        self.tree.column("Size", width=100, anchor="center")
        self.tree.column("Type", width=100, anchor="center")
        scroll = ttk.Scrollbar(
            self, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)
        self.root_path = os.getcwd()
        self.populate_tree(self.root_path)

    def browse_root(self):
        chosen = filedialog.askdirectory()
        if chosen:
            self.root_path = chosen
            self.populate_tree(self.root_path)

    def populate_tree(self, path, search_query=""):
        self.tree.delete(*self.tree.get_children())
        query = search_query.lower()
        try:
            for item in sorted(os.listdir(path)):
                full_path = os.path.join(path, item)
                if query and query not in item.lower():
                    continue
                if os.path.isdir(full_path):
                    self.tree.insert(
                        "",
                        tk.END,
                        text=f"[DIR] {item}",
                        values=("--", "Folder"),
                    )
                else:
                    size_kb = os.path.getsize(full_path) // 1024
                    ext = os.path.splitext(item)[1] or "File"
                    self.tree.insert(
                        "", tk.END, text=item, values=(f"{size_kb:,} KB", ext)
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read directory: {e}")

    def filter_tree(self, event):
        q = self.search_entry.get().strip()
        self.populate_tree(self.root_path, search_query=q)


if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()
