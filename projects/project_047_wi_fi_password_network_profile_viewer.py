# Project 47: Wi-Fi Password & Network Profile Viewer
# 100 Real-World Python Projects - Anuj Kumar Saxena
import subprocess
import platform
import re
import tkinter as tk
from tkinter import ttk, messagebox


def get_wifi_profiles():
    os_type = platform.system().lower()
    profiles = []
    if os_type == "windows":
        try:
            out = subprocess.check_output(
                ["netsh", "wlan", "show", "profiles"],
                text=True,
                errors="ignore",
            )
            names = re.findall(r"All User Profile\s*:\s*(.*)", out)
            for name in names:
                name = name.strip()
                try:
                    detail = subprocess.check_output(
                        [
                            "netsh",
                            "wlan",
                            "show",
                            "profile",
                            name,
                            "key=clear",
                        ],
                        text=True,
                        errors="ignore",
                    )
                    pwd_match = re.search(r"Key Content\s*:\s*(.*)", detail)
                    pwd = (
                        pwd_match.group(1).strip()
                        if pwd_match
                        else "[Open / None]"
                    )
                except:
                    pwd = "[Protected / Inaccessible]"
                profiles.append((name, pwd))
        except Exception as e:
            profiles.append((f"Error: {e}", ""))
    else:
        profiles.append(("[Linux/macOS requires root privileges]", ""))
    return profiles


def refresh():
    tree.delete(*tree.get_children())
    data = get_wifi_profiles()
    for row in data:
        tree.insert("", tk.END, values=row)


root = tk.Tk()
root.title("Wi-Fi Password Viewer")
root.geometry("480x360")
tk.Label(
    root,
    text="WI-FI NETWORK PROFILE AUDITOR",
    font=("Arial", 15, "bold"),
    fg="#7c2d12",
).pack(pady=12)
tree = ttk.Treeview(
    root, columns=("SSID", "Password"), show="headings", height=10
)
tree.heading("SSID", text="Network SSID")
tree.heading("Password", text="Security Key")
tree.column("SSID", width=220)
tree.column("Password", width=180)
tree.pack(fill="both", expand=True, padx=20, pady=10)
tk.Button(
    root,
    text="Refresh Profiles",
    command=refresh,
    bg="#b45309",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=10,
    pady=4,
).pack(pady=8)
refresh()
root.mainloop()
