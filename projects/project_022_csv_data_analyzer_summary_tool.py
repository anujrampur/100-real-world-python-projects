# Project 22: CSV Data Analyzer & Summary Tool
# 100 Real-World Python Projects - Anuj Kumar Saxena
import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def load_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    try:
        with open(filepath, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            data = list(reader)
        if not data:
            messagebox.showwarning(
                "Empty", "The selected CSV contains no data rows."
            )
            return
        headers = reader.fieldnames
        row_count = len(data)
        # Clear existing table
        tree.delete(*tree.get_children())
        tree["columns"] = ("Metric", "Value")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Metric", width=180)
        tree.column("Value", width=220)
        tree.heading("Metric", text="Column / Metric")
        tree.heading("Value", text="Calculated Value")
        tree.insert("", tk.END, values=("Total Rows", f"{row_count:,}"))
        tree.insert("", tk.END, values=("Total Columns", len(headers)))
        for col in headers:
            values = [row[col].strip() for row in data if row[col].strip()]
            numeric_vals = []
            for v in values:
                try:
                    numeric_vals.append(float(v.replace(",", "")))
                except ValueError:
                    pass
            if len(numeric_vals) == len(values) and len(numeric_vals) > 0:
                avg = sum(numeric_vals) / len(numeric_vals)
                tree.insert(
                    "",
                    tk.END,
                    values=(f"{col} (Sum)", f"{sum(numeric_vals):,.2f}"),
                )
                tree.insert(
                    "", tk.END, values=(f"{col} (Mean)", f"{avg:,.2f}")
                )
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        f"{col} (Min / Max)",
                        f"{min(numeric_vals):g} / {max(numeric_vals):g}",
                    ),
                )
            else:
                tree.insert(
                    "",
                    tk.END,
                    values=(f"{col} (Unique)", f"{len(set(values))} values"),
                )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse CSV: {e}")


root = tk.Tk()
root.title("CSV Data Analyzer")
root.geometry("500x420")
tk.Label(
    root, text="CSV DATA ANALYZER", font=("Arial", 16, "bold"), fg="#065f46"
).pack(pady=12)
tk.Button(
    root,
    text="Select CSV File",
    command=load_csv,
    bg="#059669",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(pady=5)
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
tree = ttk.Treeview(tree_frame)
tree.pack(fill="both", expand=True)
root.mainloop()
