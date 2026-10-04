# Project 62: Student Gradebook & Relational GPA Calculator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "gradebook.db"
GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course TEXT NOT NULL,
            credits INTEGER NOT NULL,
            grade TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()


def add_student():
    name = student_entry.get().strip()
    if not name:
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    student_entry.delete(0, tk.END)
    refresh_students()


def add_grade():
    sel = student_list.curselection()
    if not sel:
        messagebox.showwarning("Select", "Select a student first.")
        return
    s_id = student_ids[sel[0]]
    course = course_entry.get().strip()
    grade = grade_combo.get()
    try:
        credits = int(credit_entry.get())
        if credits <= 0 or not course:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Enter valid course and positive credits."
        )
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO grades (student_id, course, credits, grade) VALUES (?, ?, ?, ?)",
        (s_id, course, credits, grade),
    )
    conn.commit()
    conn.close()
    course_entry.delete(0, tk.END)
    load_student_grades(s_id)


def load_student_grades(s_id):
    grade_tree.delete(*grade_tree.get_children())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT course, credits, grade FROM grades WHERE student_id = ?",
        (s_id,),
    )
    rows = c.fetchall()
    conn.close()
    total_points = 0
    total_credits = 0
    for course, credits, grade in rows:
        grade_tree.insert("", tk.END, values=(course, credits, grade))
        total_points += GRADE_POINTS.get(grade, 0.0) * credits
        total_credits += credits
    gpa = (total_points / total_credits) if total_credits > 0 else 0.0
    gpa_lbl.config(
        text=f"Calculated GPA: {gpa:.2f} (Total Credits: {total_credits})"
    )


def on_student_select(event):
    sel = student_list.curselection()
    if sel:
        load_student_grades(student_ids[sel[0]])


def refresh_students():
    student_list.delete(0, tk.END)
    global student_ids
    student_ids = []
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name FROM students")
    for sid, name in c.fetchall():
        student_list.insert(tk.END, f"{name} (ID: {sid})")
        student_ids.append(sid)
    conn.close()


init_db()
root = tk.Tk()
root.title("Student Gradebook & GPA Calculator")
root.geometry("640x440")
tk.Label(
    root,
    text="STUDENT GRADEBOOK & GPA ENGINE",
    font=("Arial", 15, "bold"),
    fg="#164e63",
).pack(pady=10)
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=15, pady=5)
# Left Column (Students)
left_f = tk.Frame(main_frame)
left_f.pack(side="left", fill="y", padx=(0, 15))
tk.Label(left_f, text="Students", font=("Arial", 11, "bold")).pack()
student_list = tk.Listbox(left_f, width=20, height=12)
student_list.pack(pady=4)
student_list.bind("<<ListboxSelect>>", on_student_select)
s_in = tk.Frame(left_f)
s_in.pack(pady=4)
student_entry = tk.Entry(s_in, width=12)
student_entry.pack(side="left", padx=2)
tk.Button(s_in, text="+ Add", command=add_student).pack(side="left")
# Right Column (Grades & GPA)
right_f = tk.Frame(main_frame)
right_f.pack(side="right", fill="both", expand=True)
g_in = tk.Frame(right_f)
g_in.pack(pady=4)
course_entry = tk.Entry(g_in, width=14)
course_entry.pack(side="left", padx=2)
credit_entry = tk.Entry(g_in, width=5)
credit_entry.pack(side="left", padx=2)
credit_entry.insert(0, "3")
grade_combo = ttk.Combobox(
    g_in, values=["A", "B", "C", "D", "F"], width=4, state="readonly"
)
grade_combo.pack(side="left", padx=2)
grade_combo.set("A")
tk.Button(
    g_in, text="Add Grade", command=add_grade, bg="#0891b2", fg="white"
).pack(side="left", padx=4)
grade_tree = ttk.Treeview(
    right_f, columns=("Course", "Credits", "Grade"), show="headings", height=8
)
grade_tree.heading("Course", text="Course Title")
grade_tree.column("Course", width=180)
grade_tree.heading("Credits", text="Credits")
grade_tree.column("Credits", width=70, anchor="center")
grade_tree.heading("Grade", text="Grade")
grade_tree.column("Grade", width=60, anchor="center")
grade_tree.pack(fill="both", expand=True, pady=6)
gpa_lbl = tk.Label(
    right_f,
    text="Calculated GPA: 0.00",
    font=("Arial", 11, "bold"),
    fg="#0e7490",
)
gpa_lbl.pack(pady=4)
refresh_students()
root.mainloop()
