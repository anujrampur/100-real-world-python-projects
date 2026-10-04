# Project 94: Continuous Integration (CI) Test Runner Bot
# 100 Real-World Python Projects - Anuj Kumar Saxena
import subprocess
import os
import sys
import threading
import tkinter as tk
from tkinter import messagebox


class CIRunner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Continuous Integration (CI) Test Runner")
        self.geometry("580x420")
        tk.Label(
            self,
            text="CONTINUOUS INTEGRATION (CI) RUNNER",
            font=("Arial", 15, "bold"),
            fg="#1e3a8a",
        ).pack(pady=12)
        ctrl_f = tk.Frame(self)
        ctrl_f.pack(pady=4)
        self.btn_run = tk.Button(
            ctrl_f,
            text="Execute Test Suite",
            command=self.run_tests,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=4,
        )
        self.btn_run.pack(side="left", padx=6)
        self.status_lbl = tk.Label(
            self,
            text="Build Status: IDLE",
            font=("Arial", 11, "bold"),
            fg="#64748b",
        )
        self.status_lbl.pack(pady=6)
        self.output_text = tk.Text(
            self, height=13, width=64, font=("Consolas", 9), bg="#f8fafc"
        )
        self.output_text.pack(padx=20, pady=8)

    def run_tests(self):
        self.btn_run.config(state="disabled")
        self.status_lbl.config(
            text="Build Status: RUNNING TESTS...", fg="#0284c7"
        )
        self.output_text.delete("1.0", tk.END)

        def worker():
            # Run built-in test runner on sample inline tests
            cmd = [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                ".",
                "-p",
                "*test*.py",
            ]
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = proc.communicate()
                output = stdout + stderr
                self.output_text.insert(
                    tk.END,
                    (
                        output
                        if output.strip()
                        else "Ran 0 tests (No *test*.py files found in current directory).\n"
                    ),
                )
                if proc.returncode == 0:
                    self.status_lbl.config(
                        text="BUILD PASSED (Exit Code: 0)", fg="#15803d"
                    )
                else:
                    self.status_lbl.config(
                        text="BUILD FAILED (Test Failures Detected)",
                        fg="#dc2626",
                    )
            except Exception as e:
                self.output_text.insert(tk.END, f"Execution error: {e}")
                self.status_lbl.config(text="BUILD ERROR", fg="#dc2626")
            self.btn_run.config(state="normal")

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    app = CIRunner()
    app.mainloop()
