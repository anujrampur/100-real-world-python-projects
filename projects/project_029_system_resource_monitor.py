import os
import platform
import shutil
import time
import tkinter as tk
from tkinter import ttk

REFRESH_MS = 1000
IS_WINDOWS = platform.system() == "Windows"
prev_cpu = None  # previous (idle, total) sample, needed to compute CPU %


def read_cpu_times():
    """Return (idle, total) CPU time counters, or None if unavailable."""
    try:
        if IS_WINDOWS:
            import ctypes

            class FILETIME(ctypes.Structure):
                _fields_ = [
                    ("low", ctypes.c_ulong),
                    ("high", ctypes.c_ulong),
                ]

            idle, kernel, user = FILETIME(), FILETIME(), FILETIME()
            ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)
            )
            val = lambda t: (t.high << 32) | t.low
            # Windows: kernel time already includes idle time
            return val(idle), val(kernel) + val(user)
        with open("/proc/stat") as f:  # Linux
            parts = [int(x) for x in f.readline().split()[1:9]]
        return parts[3] + parts[4], sum(parts)
    except Exception:
        return None


def cpu_percent():
    """CPU load since the previous call, as a number 0-100 (or None)."""
    global prev_cpu
    now = read_cpu_times()
    if now is None:
        return None
    last, prev_cpu = prev_cpu, now
    if last is None:
        return None  # first call: nothing to compare with yet
    idle_delta, total_delta = now[0] - last[0], now[1] - last[1]
    if total_delta <= 0:
        return None
    return max(0.0, min(100.0, 100.0 * (1 - idle_delta / total_delta)))


def memory_info():
    """Return (used_bytes, total_bytes) of physical RAM, or None."""
    try:
        if IS_WINDOWS:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(stat)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return stat.ullTotalPhys - stat.ullAvailPhys, stat.ullTotalPhys
        info = {}
        with open("/proc/meminfo") as f:  # Linux
            for line in f:
                key, value = line.split(":")
                info[key] = int(value.split()[0]) * 1024
        return info["MemTotal"] - info["MemAvailable"], info["MemTotal"]
    except Exception:
        return None


def update_metrics():
    # CPU
    cpu = cpu_percent()
    if cpu is not None:
        cpu_bar["value"] = cpu
        cpu_label.config(text=f"CPU Load: {cpu:.0f}%")
    elif prev_cpu is None:
        cpu_label.config(text="CPU Load: not available on this system")
    else:
        cpu_label.config(text="CPU Load: measuring...")
    # RAM
    mem = memory_info()
    if mem:
        used, total = mem
        pct = used / total * 100
        ram_bar["value"] = pct
        ram_label.config(
            text=f"RAM Usage: {pct:.0f}% "
            f"({used / 2**30:.1f} GB / {total / 2**30:.1f} GB)"
        )
    else:
        ram_label.config(text="RAM Usage: not available on this system")
    # Disk
    total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
    disk_pct = used / total * 100
    disk_bar["value"] = disk_pct
    disk_label.config(
        text=f"Disk Usage: {disk_pct:.0f}% "
        f"({used // 2**30} GB / {total // 2**30} GB)"
    )
    # Static info and a visible refresh clock
    info_label.config(
        text=f"{platform.system()} {platform.release()} | "
        f"{platform.machine()} | {os.cpu_count() or 1} logical cores"
    )
    clock_label.config(text="Last update: " + time.strftime("%H:%M:%S"))
    root.after(REFRESH_MS, update_metrics)


root = tk.Tk()
root.title("System Resource Monitor")
root.geometry("460x360")
tk.Label(
    root,
    text="SYSTEM RESOURCE MONITOR",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=12)
info_label = tk.Label(root, text="", font=("Arial", 9), fg="#4a5568")
info_label.pack(pady=2)
frame = tk.Frame(root, padx=20, pady=6)
frame.pack(fill="both", expand=True)


def add_meter(name):
    label = tk.Label(
        frame, text=f"{name}: ...", font=("Arial", 10, "bold"), anchor="w"
    )
    label.pack(fill="x", pady=(8, 2))
    bar = ttk.Progressbar(
        frame, orient="horizontal", length=380, mode="determinate"
    )
    bar.pack()
    return label, bar


cpu_label, cpu_bar = add_meter("CPU Load")
ram_label, ram_bar = add_meter("RAM Usage")
disk_label, disk_bar = add_meter("Disk Usage")
clock_label = tk.Label(root, text="", font=("Arial", 9), fg="#4a5568")
clock_label.pack(pady=8)
root.after(200, update_metrics)
root.mainloop()
