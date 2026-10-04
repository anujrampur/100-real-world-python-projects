# Project 25: Excel Spreadsheet Automator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox, filedialog
import zipfile
from xml.sax.saxutils import escape


def col_letter(i):
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]


def make_sheet_xml(rows):
    """rows: list of lists. A cell is text, a number, or ('formula', 'C2*D2', cached_value)."""
    out = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>',
    ]
    for r, row in enumerate(rows, 1):
        out.append(f'<row r="{r}">')
        for c, val in enumerate(row):
            ref = f"{col_letter(c)}{r}"
            if isinstance(val, tuple):
                out.append(
                    f'<c r="{ref}"><f>{escape(val[1])}</f><v>{val[2]}</v></c>'
                )
            elif isinstance(val, (int, float)):
                out.append(f'<c r="{ref}"><v>{val}</v></c>')
            elif val != "":
                out.append(
                    f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(val))}</t></is></c>'
                )
        out.append("</row>")
    out.append("</sheetData></worksheet>")
    return "".join(out)


def write_xlsx(path, rows, sheet_name="Sales"):
    ct = (
        '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'
    )
    wb = (
        '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets><sheet name="{escape(sheet_name)}" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>'
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/worksheets/sheet1.xml", make_sheet_xml(rows))


def create_excel_report():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx", filetypes=[("Excel Workbook", "*.xlsx")]
    )
    if not save_path:
        return
    products = [
        ("Keyboard", "North", 45, 25.00),
        ("Mouse", "South", 80, 15.50),
        ("Monitor", "East", 20, 180.00),
        ("Headset", "West", 60, 42.00),
        ("Webcam", "North", 35, 55.00),
    ]
    data = [
        ["Product", "Region", "Units Sold", "Unit Price", "Total Revenue"]
    ]
    for i, (name, region, units, price) in enumerate(products, 2):
        data.append(
            [
                name,
                region,
                units,
                price,
                ("formula", f"C{i}*D{i}", units * price),
            ]
        )
    total_units = sum(p[2] for p in products)
    total_sales = sum(p[2] * p[3] for p in products)
    data.append(
        [
            "Total Units",
            "",
            ("formula", "SUM(C2:C6)", total_units),
            "Total Sales:",
            ("formula", "SUM(E2:E6)", total_sales),
        ]
    )
    try:
        write_xlsx(save_path, data)
        messagebox.showinfo(
            "Success",
            f"Excel workbook created at:\n{save_path}\n\nLive formulas included!",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save workbook: {e}")


root = tk.Tk()
root.title("Excel Spreadsheet Automator")
root.geometry("420x240")
tk.Label(
    root,
    text="SPREADSHEET AUTOMATOR",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=15)
tk.Label(
    root,
    text="Generates a real .xlsx sales workbook\nwith live spreadsheet formulas.",
    font=("Arial", 10),
    justify="center",
).pack(pady=5)
tk.Button(
    root,
    text="Generate Excel Workbook",
    command=create_excel_report,
    bg="#059669",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=12,
    pady=6,
).pack(pady=20)
root.mainloop()
