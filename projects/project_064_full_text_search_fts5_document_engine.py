# Project 64: Full-Text Search (FTS5) Document Engine
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "documents_fts.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(
            title,
            body
        )
    """)
    # Seed sample articles if empty
    c.execute("SELECT COUNT(*) FROM docs")
    if c.fetchone()[0] == 0:
        sample_docs = [
            (
                "Python Programming Overview",
                "Python is an interpreted, high-level language emphasizing readability and simplicity.",
            ),
            (
                "Relational Databases and SQL",
                "SQL is a standard language for storing, manipulating and retrieving data in databases.",
            ),
            (
                "Full-Text Search Architecture",
                "Full-text search engines index textual tokens to allow fast keyword retrieval and ranking.",
            ),
            (
                "Machine Learning Fundamentals",
                "Machine learning algorithms build mathematical models based on sample training data.",
            ),
        ]
        c.executemany(
            "INSERT INTO docs (title, body) VALUES (?, ?)", sample_docs
        )
    conn.commit()
    conn.close()


def add_document():
    title = title_entry.get().strip()
    body = body_text.get("1.0", tk.END).strip()
    if not title or not body:
        messagebox.showwarning("Warning", "Title and Body are required.")
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO docs (title, body) VALUES (?, ?)", (title, body))
    conn.commit()
    conn.close()
    title_entry.delete(0, tk.END)
    body_text.delete("1.0", tk.END)
    messagebox.showinfo("Indexed", "Document added to FTS index!")
    search_docs()


def search_docs():
    query = search_entry.get().strip()
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if query:
        # FTS5 MATCH query with BM25 ranking
        try:
            c.execute(
                """
                SELECT title, snippet(docs, 1, '[', ']', '...', 10), bm25(docs)
                FROM docs WHERE docs MATCH ? ORDER BY bm25(docs)
            """,
                (query,),
            )
            rows = c.fetchall()
        except sqlite3.OperationalError:
            rows = []
    else:
        c.execute("SELECT title, substr(body, 1, 60) || '...', 0.0 FROM docs")
        rows = c.fetchall()
    conn.close()
    for r in rows:
        tree.insert("", tk.END, values=(r[0], r[1], f"{r[2]:.2f}"))


init_db()
root = tk.Tk()
root.title("Full-Text Search Engine (FTS5)")
root.geometry("640x480")
tk.Label(
    root,
    text="SQLITE FTS5 FULL-TEXT SEARCH ENGINE",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=10)
# Search bar
s_frame = tk.Frame(root)
s_frame.pack(fill="x", padx=20, pady=5)
tk.Label(s_frame, text="Search Keywords:").pack(side="left", padx=4)
search_entry = tk.Entry(s_frame, width=32, font=("Arial", 10))
search_entry.pack(side="left", padx=4)
search_entry.bind("<KeyRelease>", lambda e: search_docs())
tk.Button(
    s_frame, text="Search", command=search_docs, bg="#0891b2", fg="white"
).pack(side="left", padx=4)
tree = ttk.Treeview(
    root, columns=("Title", "Snippet", "Rank"), show="headings", height=7
)
tree.heading("Title", text="Document Title")
tree.column("Title", width=200)
tree.heading("Snippet", text="Matched Snippet")
tree.column("Snippet", width=340)
tree.heading("Rank", text="BM25 Score")
tree.column("Rank", width=70, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=6)
# Add Document Panel
add_box = tk.LabelFrame(root, text="Index New Document", padx=10, pady=6)
add_box.pack(fill="x", padx=20, pady=8)
tk.Label(add_box, text="Title:").pack(anchor="w")
title_entry = tk.Entry(add_box, width=45)
title_entry.pack(fill="x", pady=2)
tk.Label(add_box, text="Body:").pack(anchor="w")
body_text = tk.Text(add_box, height=3, width=45)
body_text.pack(fill="x", pady=2)
tk.Button(
    add_box,
    text="Add & Index Document",
    command=add_document,
    bg="#0891b2",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(pady=4)
search_docs()
root.mainloop()
