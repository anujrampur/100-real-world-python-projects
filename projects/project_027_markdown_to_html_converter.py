# Project 27: Markdown to HTML Converter
# 100 Real-World Python Projects - Anuj Kumar Saxena
import re
import tkinter as tk


def md_to_html(md):
    lines = md.split("\n")
    html_lines = []
    in_list = False
    for line in lines:
        # Headers
        if line.startswith("### "):
            line = f"<h3>{line[4:]}</h3>"
        elif line.startswith("## "):
            line = f"<h2>{line[3:]}</h2>"
        elif line.startswith("# "):
            line = f"<h1>{line[2:]}</h1>"
        # Bullet list
        elif line.startswith("* ") or line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            line = f"  <li>{line[2:]}</li>"
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if line.strip():
                line = f"<p>{line}</p>"
        # Inline formatting: bold, italic, code
        line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\*(.*?)\*", r"<em>\1</em>", line)
        line = re.sub(r"`(.*?)`", r"<code>\1</code>", line)
        html_lines.append(line)
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def convert():
    raw_md = txt_input.get("1.0", tk.END)
    converted = md_to_html(raw_md)
    txt_output.delete("1.0", tk.END)
    txt_output.insert(tk.END, converted)


root = tk.Tk()
root.title("Markdown to HTML Converter")
root.geometry("680x440")
tk.Label(
    root,
    text="MARKDOWN TO HTML CONVERTER",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=10)
panes = tk.Frame(root)
panes.pack(fill="both", expand=True, padx=15, pady=5)
txt_input = tk.Text(panes, width=38, height=16, font=("Consolas", 10))
txt_input.pack(side="left", fill="both", expand=True, padx=4)
txt_input.insert(
    tk.END,
    "# Welcome\n\nThis is **bold** and *italic* text.\n\n* Point 1\n* Point 2\n\nUse `print()` in Python.",
)
txt_output = tk.Text(
    panes, width=38, height=16, font=("Consolas", 10), bg="#f8fafc"
)
txt_output.pack(side="left", fill="both", expand=True, padx=4)
tk.Button(
    root,
    text="Compile to HTML",
    command=convert,
    bg="#059669",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=5,
).pack(pady=10)
convert()
root.mainloop()
