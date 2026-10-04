# Project 30: REST API Weather & Forecast Desk
# 100 Real-World Python Projects - Anuj Kumar Saxena
import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.parse
import json

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search?name={}&count=1"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}¤t_weather=true"


def fetch_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Enter a city name.")
        return
    try:
        # Step 1: Geocoding coordinates lookup
        req_geo = urllib.request.Request(
            GEO_URL.format(urllib.parse.quote(city)),
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req_geo, timeout=6) as resp:
            geo_data = json.loads(resp.read().decode())
        if "results" not in geo_data:
            messagebox.showerror("Not Found", f"City '{city}' not found.")
            return
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        country = geo_data["results"][0].get("country", "")
        # Step 2: Fetch current weather for coordinates
        req_w = urllib.request.Request(
            WEATHER_URL.format(lat, lon),
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req_w, timeout=6) as resp:
            w_data = json.loads(resp.read().decode())
        current = w_data["current_weather"]
        temp = current["temperature"]
        wind = current["windspeed"]
        res_city.config(text=f"{city.title()}, {country}")
        res_temp.config(text=f"{temp}°C")
        res_details.config(
            text=f"Wind Speed: {wind} km/h | Coordinates: ({lat:.2f}, {lon:.2f})"
        )
    except Exception as e:
        messagebox.showerror("API Error", f"Unable to retrieve weather: {e}")


root = tk.Tk()
root.title("Weather Desk")
root.geometry("450x360")
tk.Label(
    root,
    text="WEATHER & FORECAST DESK",
    font=("Arial", 16, "bold"),
    fg="#065f46",
).pack(pady=15)
search_f = tk.Frame(root)
search_f.pack(pady=5)
city_entry = tk.Entry(
    search_f, width=22, font=("Arial", 12), justify="center"
)
city_entry.pack(side="left", padx=5)
city_entry.insert(0, "London")
tk.Button(
    search_f,
    text="Get Weather",
    command=fetch_weather,
    bg="#059669",
    fg="white",
    font=("Arial", 10, "bold"),
).pack(side="left")
card = tk.Frame(root, bg="#f8fafc", bd=1, relief="solid", padx=20, pady=15)
card.pack(fill="both", expand=True, padx=30, pady=15)
res_city = tk.Label(
    card, text="Search for a city", font=("Arial", 14, "bold"), bg="#f8fafc"
)
res_city.pack(pady=4)
res_temp = tk.Label(
    card, text="--°C", font=("Arial", 36, "bold"), fg="#059669", bg="#f8fafc"
)
res_temp.pack(pady=5)
res_details = tk.Label(
    card, text="", font=("Arial", 10), fg="#64748b", bg="#f8fafc"
)
res_details.pack(pady=4)
root.bind("<Return>", lambda e: fetch_weather())
root.mainloop()
