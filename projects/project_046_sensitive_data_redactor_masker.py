# Project 46: Sensitive Data Redactor & Masker
# 100 Real-World Python Projects - Anuj Kumar Saxena
import re
import tkinter as tk

PII_PATTERNS = {
    "Credit Card": (
        r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b",
        "[REDACTED-CARD]",
    ),
    "Social Security / National ID": (
        r"\b\d{3}-\d{2}-\d{4}\b",
        "[REDACTED-SSN]",
    ),
    "Email Address": (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "[REDACTED-EMAIL]",
    ),
    "API Key / Secret": (
        r"\b(?:sk_live_|AKIA)[0-9a-zA-Z]{16,}\b",
        "[REDACTED-APIKEY]",
    ),
    "IPv4 Address": (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED-IP]"),
}


def redact_text():
    content = input_text.get("1.0", tk.END)
    redacted = content
    counts = {}
    for label, (pattern, replacement) in PII_PATTERNS.items():
        matches = re.findall(pattern, redacted)
        counts[label] = len(matches)
        redacted = re.sub(pattern, replacement, redacted)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, redacted)
    report = " | ".join([f"{k}: {v}" for k, v in counts.items() if v > 0])
    stats_lbl.config(
        text=f"Redactions Found -> {report if report else 'No PII Detected'}"
    )


root = tk.Tk()
root.title("Sensitive Data Redactor")
root.geometry("620x460")
tk.Label(
    root,
    text="SENSITIVE DATA & PII REDACTOR",
    font=("Arial", 16, "bold"),
    fg="#7c2d12",
).pack(pady=10)
tk.Label(root, text="Original Text (with sensitive data):").pack(
    anchor="w", padx=20
)
input_text = tk.Text(root, height=7, width=68, font=("Consolas", 9))
input_text.pack(padx=20, pady=4)
input_text.insert(
    tk.END,
    "Customer John Doe (email: john.doe@sample.com) bought items.\nCard: 4111111111111111, SSN: 123-45-6789.\nServer IP: 192.168.1.50 with AWS Key: AKIA1234567890ABCDEF.",
)
tk.Button(
    root,
    text="Redact PII Elements",
    command=redact_text,
    bg="#b45309",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=4,
).pack(pady=8)
stats_lbl = tk.Label(
    root,
    text="Click Redact to analyze",
    font=("Arial", 9, "bold"),
    fg="#0369a1",
)
stats_lbl.pack()
tk.Label(root, text="Sanitized / Redacted Output:").pack(anchor="w", padx=20)
output_text = tk.Text(
    root, height=7, width=68, font=("Consolas", 9), bg="#f8fafc"
)
output_text.pack(padx=20, pady=4)
root.mainloop()
