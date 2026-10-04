# Project 91: Enterprise Point-of-Sale (POS) & Retail Billing Terminal
# 100 Real-World Python Projects - Anuj Kumar Saxena
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB_NAME = "pos_enterprise.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            total_amount REAL
        )
    """)
    # Seed default inventory
    sample_items = [
        (101, "Wireless Mouse", 25.00, 50),
        (102, "Mechanical Keyboard", 85.00, 30),
        (103, "USB-C Hub", 35.00, 40),
        (104, "Gaming Headset", 65.00, 20),
    ]
    c.executemany(
        "INSERT OR IGNORE INTO inventory VALUES (?, ?, ?, ?)", sample_items
    )
    conn.commit()
    conn.close()


cart = []


class POSTerminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enterprise POS Billing Terminal")
        self.geometry("720x520")
        tk.Label(
            self,
            text="ENTERPRISE POINT-OF-SALE (POS)",
            font=("Arial", 16, "bold"),
            fg="#1e3a8a",
        ).pack(pady=10)
        # Scanner Frame
        scan_f = tk.LabelFrame(
            self, text="Item Lookup / Barcode Entry", padx=10, pady=6
        )
        scan_f.pack(fill="x", padx=20, pady=5)
        tk.Label(scan_f, text="Product ID:").pack(side="left", padx=4)
        self.id_entry = tk.Entry(scan_f, width=10)
        self.id_entry.pack(side="left", padx=4)
        self.id_entry.insert(0, "101")
        tk.Label(scan_f, text="Qty:").pack(side="left", padx=4)
        self.qty_entry = tk.Entry(scan_f, width=6)
        self.qty_entry.pack(side="left", padx=4)
        self.qty_entry.insert(0, "1")
        tk.Button(
            scan_f,
            text="+ Add to Cart",
            command=self.add_to_cart,
            bg="#2563eb",
            fg="white",
            font=("Arial", 9, "bold"),
        ).pack(side="left", padx=8)
        # Cart Table
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Name", "Price", "Qty", "Subtotal"),
            show="headings",
            height=10,
        )
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=60, anchor="center")
        self.tree.heading("Name", text="Product Description")
        self.tree.column("Name", width=240)
        self.tree.heading("Price", text="Unit Price")
        self.tree.column("Price", width=90, anchor="center")
        self.tree.heading("Qty", text="Quantity")
        self.tree.column("Qty", width=80, anchor="center")
        self.tree.heading("Subtotal", text="Total ($)")
        self.tree.column("Subtotal", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        # Checkout Bottom Bar
        b_bar = tk.Frame(self, padx=20, pady=10)
        b_bar.pack(fill="x")
        self.total_lbl = tk.Label(
            b_bar,
            text="Grand Total: $0.00",
            font=("Arial", 14, "bold"),
            fg="#15803d",
        )
        self.total_lbl.pack(side="left")
        tk.Button(
            b_bar,
            text="Complete Checkout & Print",
            command=self.checkout,
            bg="#15803d",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=4,
        ).pack(side="right")
        tk.Button(
            b_bar, text="Clear Cart", command=self.clear_cart, fg="#dc2626"
        ).pack(side="right", padx=10)

    def add_to_cart(self):
        try:
            pid = int(self.id_entry.get().strip())
            qty = int(self.qty_entry.get().strip())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Enter valid numeric product ID and quantity."
            )
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "SELECT name, price, stock FROM inventory WHERE id = ?", (pid,)
        )
        row = c.fetchone()
        conn.close()
        if not row:
            messagebox.showerror(
                "Not Found", f"No product found with ID {pid}."
            )
            return
        name, price, stock = row
        if stock < qty:
            messagebox.showwarning(
                "Stock Alert",
                f"Insufficient inventory! Only {stock} units available.",
            )
            return
        subtotal = price * qty
        cart.append(
            {
                "id": pid,
                "name": name,
                "price": price,
                "qty": qty,
                "subtotal": subtotal,
            }
        )
        self.refresh_cart()

    def refresh_cart(self):
        self.tree.delete(*self.tree.get_children())
        grand_total = 0.0
        for item in cart:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item["id"],
                    item["name"],
                    f"${item['price']:.2f}",
                    item["qty"],
                    f"${item['subtotal']:.2f}",
                ),
            )
            grand_total += item["subtotal"]
        self.total_lbl.config(text=f"Grand Total: ${grand_total:.2f}")

    def clear_cart(self):
        cart.clear()
        self.refresh_cart()

    def checkout(self):
        if not cart:
            messagebox.showwarning(
                "Cart Empty", "Add items to cart prior to checkout."
            )
            return
        grand_total = sum(i["subtotal"] for i in cart)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            # Atomic checkout transaction
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "INSERT INTO sales (timestamp, total_amount) VALUES (?, ?)",
                (ts, grand_total),
            )
            for item in cart:
                c.execute(
                    "UPDATE inventory SET stock = stock - ? WHERE id = ?",
                    (item["qty"], item["id"]),
                )
            conn.commit()
            messagebox.showinfo(
                "Receipt Printed",
                f"Payment successful!\nTotal: ${grand_total:.2f}\nInventory updated.",
            )
            self.clear_cart()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Transaction Error", f"Checkout failed: {e}")
        finally:
            conn.close()


init_db()
if __name__ == "__main__":
    app = POSTerminal()
    app.mainloop()
