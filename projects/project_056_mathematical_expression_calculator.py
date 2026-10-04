# Project 56: Mathematical Expression Calculator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
import math
import re


class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Expression Calculator")
        self.geometry("360x480")
        self.resizable(False, False)
        self.expression = ""
        # Display screen
        self.display = tk.Entry(
            self,
            font=("Consolas", 20, "bold"),
            justify="right",
            bd=10,
            relief="flat",
            bg="#f8fafc",
        )
        self.display.pack(fill="x", padx=15, pady=15)
        self.display.insert(0, "0")
        # Buttons layout
        btn_layout = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "sqrt", "="],
        ]
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="both", expand=True, padx=10, pady=5)
        for r, row in enumerate(btn_layout):
            btn_frame.grid_rowconfigure(r, weight=1)
            for c, char in enumerate(row):
                btn_frame.grid_columnconfigure(c, weight=1)
                cmd = lambda ch=char: self.on_press(ch)
                bg_col = (
                    "#e2e8f0"
                    if char not in ["=", "C"]
                    else ("#2563eb" if char == "=" else "#fee2e2")
                )
                fg_col = (
                    "#ffffff"
                    if char == "="
                    else ("#991b1b" if char == "C" else "#0f172a")
                )
                btn = tk.Button(
                    btn_frame,
                    text=char,
                    font=("Arial", 12, "bold"),
                    bg=bg_col,
                    fg=fg_col,
                    command=cmd,
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

    def on_press(self, char):
        if char == "C":
            self.expression = ""
            self.update_display("0")
        elif char == "=":
            self.calculate()
        elif char == "sqrt":
            try:
                val = float(self.display.get())
                if val < 0:
                    raise ValueError
                res = math.sqrt(val)
                self.expression = str(res)
                self.update_display(f"{res:.6g}")
            except Exception:
                self.update_display("Error")
                self.expression = ""
        else:
            if self.expression == "" and char in "0123456789":
                self.expression = char
            else:
                self.expression += char
            self.update_display(self.expression)

    def calculate(self):
        try:
            # Evaluate only after the whitelist check below
            sanitized = self.expression.replace("^", "**")
            # Only digits, operators, brackets, dots and spaces may reach eval()
            if len(sanitized) > 200 or not re.fullmatch(
                r"[0-9+\-*/(). %e]*", sanitized
            ):
                raise ValueError("unsafe expression")
            result = eval(sanitized, {"__builtins__": None}, {})
            self.update_display(f"{result:.8g}")
            self.expression = str(result)
        except ZeroDivisionError:
            self.update_display("Division by Zero")
            self.expression = ""
        except Exception:
            self.update_display("Invalid Syntax")
            self.expression = ""

    def update_display(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(0, text)


if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
