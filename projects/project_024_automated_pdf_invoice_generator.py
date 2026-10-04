# Project 24: Automated PDF Invoice Generator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime

items = []


def build_pdf(lines):
    """Build a minimal single-page PDF (Courier 10pt) using only the standard library."""

    def esc(s):
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    content = ["BT", "/F1 10 Tf", "13 TL", "50 790 Td"]
    for line in lines:
        content.append(f"({esc(line)}) Tj T*")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length "
        + str(len(stream)).encode()
        + b" >>\nstream\n"
        + stream
        + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for off in offsets:
        pdf += f"{off:010d} 00000 n \n".encode()
    pdf += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(pdf)


def add_item():
    name = item_name.get().strip()
    try:
        qty = int(item_qty.get())
        price = float(item_price.get())
        if not name or qty <= 0 or price <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Error", "Enter a name, valid quantity and price."
        )
        return
    items.append(
        {"name": name, "qty": qty, "price": price, "total": qty * price}
    )
    listbox.insert(
        tk.END, f"{name} - {qty} x ${price:.2f} = ${qty * price:.2f}"
    )
    item_name.delete(0, tk.END)
    item_qty.delete(0, tk.END)
    item_price.delete(0, tk.END)


def generate_invoice():
    client = client_entry.get().strip()
    if not client or not items:
        messagebox.showerror("Error", "Client name and items required.")
        return
    subtotal = sum(i["total"] for i in items)
    tax = subtotal * 0.10
    grand_total = subtotal + tax
    inv_date = datetime.now().strftime("%d-%m-%Y")
    report = [
        "=" * 60,
        f"INVOICE FOR: {client}",
        f"DATE: {inv_date}",
        "=" * 60,
        f"{'ITEM':<26}{'QTY':>5}{'PRICE':>13}{'TOTAL':>14}",
        "-" * 60,
    ]
    for i in items:
        report.append(
            f"{i['name'][:25]:<26}{i['qty']:>5}{i['price']:>13.2f}{i['total']:>14.2f}"
        )
    report.extend(
        [
            "-" * 60,
            f"{'Subtotal:':<44}{subtotal:>16.2f}",
            f"{'Tax (10%):':<44}{tax:>16.2f}",
            f"{'Grand Total:':<44}{grand_total:>16.2f}",
            "=" * 60,
        ]
    )
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF document", "*.pdf")]
    )
    if save_path:
        with open(save_path, "wb") as f:
            f.write(build_pdf(report))
        messagebox.showinfo("Success", f"Invoice PDF saved to:\n{save_path}")


root = tk.Tk()
root.title("Invoice Generator")
root.geometry("450x450")
tk.Label(
    root,
    text="PDF INVOICE GENERATOR",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=10)
client_entry = tk.Entry(root, width=32)
client_entry.pack(pady=5)
client_entry.insert(0, "Acme Corporation")
frame = tk.Frame(root)
frame.pack(pady=5)
item_name = tk.Entry(frame, width=14)
item_name.pack(side="left", padx=2)
item_qty = tk.Entry(frame, width=5)
item_qty.pack(side="left", padx=2)
item_price = tk.Entry(frame, width=8)
item_price.pack(side="left", padx=2)
tk.Button(frame, text="Add Item", command=add_item).pack(side="left", padx=4)
listbox = tk.Listbox(root, width=48, height=8)
listbox.pack(pady=10)
tk.Button(
    root,
    text="Export Invoice as PDF",
    command=generate_invoice,
    bg="#059669",
    fg="white",
    font=("Arial", 11, "bold"),
    pady=5,
).pack(pady=10)
root.mainloop()
