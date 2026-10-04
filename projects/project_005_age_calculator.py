# Project 5: Age Calculator
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
import calendar


def calculate_age_components(dob, today):
    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day
    if days < 0:
        months -= 1
        previous_month = today.month - 1
        previous_year = today.year
        if previous_month == 0:
            previous_month = 12
            previous_year -= 1
        days += calendar.monthrange(previous_year, previous_month)[1]
    if months < 0:
        years -= 1
        months += 12
    return years, months, days


def get_next_birthday(dob, today):
    year = today.year
    if dob.month == 2 and dob.day == 29:
        next_birthday = (
            date(year, 2, 29) if calendar.isleap(year) else date(year, 2, 28)
        )
    else:
        next_birthday = date(year, dob.month, dob.day)
    if next_birthday < today:
        year += 1
        if dob.month == 2 and dob.day == 29:
            next_birthday = (
                date(year, 2, 29)
                if calendar.isleap(year)
                else date(year, 2, 28)
            )
        else:
            next_birthday = date(year, dob.month, dob.day)
    return next_birthday


def calculate_age():
    try:
        dob = datetime.strptime(dob_entry.get().strip(), "%d-%m-%Y").date()
    except ValueError:
        messagebox.showerror("Invalid Date", "Use DD-MM-YYYY format.")
        return
    today = date.today()
    if dob > today:
        messagebox.showerror(
            "Invalid Date", "Date of birth cannot be in the future."
        )
        return
    years, months, days = calculate_age_components(dob, today)
    total_days = (today - dob).days
    next_birthday = get_next_birthday(dob, today)
    days_until = (next_birthday - today).days
    result.set(
        f"Date of Birth: {dob:%d-%m-%Y}\n"
        f"Today's Date: {today:%d-%m-%Y}\n\n"
        f"Age: {years} Years, {months} Months, {days} Days\n"
        f"Total Lived Days: {total_days:,}\n\n"
        f"Next Birthday: {next_birthday:%d-%m-%Y}\n"
        f"Days Until Birthday: {days_until} Days"
    )


def clear_all():
    dob_entry.delete(0, tk.END)
    result.set("")


root = tk.Tk()
root.title("Age Calculator")
root.geometry("450x450")
tk.Label(root, text="AGE CALCULATOR", font=("Arial", 18, "bold")).pack(
    pady=15
)
tk.Label(root, text="Date of Birth (DD-MM-YYYY)").pack()
dob_entry = tk.Entry(root, width=20, justify="center")
dob_entry.pack(pady=6)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Calculate Age", command=calculate_age).pack(
    side="left", padx=5
)
tk.Button(btn_frame, text="Clear", command=clear_all).pack(
    side="left", padx=5
)
result = tk.StringVar()
tk.Label(root, textvariable=result, font=("Arial", 10), justify="left").pack(
    pady=15
)
root.mainloop()
