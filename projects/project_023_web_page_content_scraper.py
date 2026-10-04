# Project 23: Web Page Content Scraper
# 100 Real-World Python Projects - Anuj Kumar Saxena
import urllib.request
from html.parser import HTMLParser
import tkinter as tk
from tkinter import messagebox


class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.links = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v.startswith("http"):
                    self.links.append(v)

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned and self.current_tag in ["h1", "h2", "title"]:
            self.headings.append(f"[{self.current_tag.upper()}] {cleaned}")

    def handle_endtag(self, tag):
        self.current_tag = None


def scrape_url():
    url = url_entry.get().strip()
    if not url.startswith("http"):
        messagebox.showerror(
            "Invalid URL",
            "Please enter a URL starting with http:// or https://",
        )
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Scraping: {url}\n" + "=" * 50 + "\n\n")
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        parser = ContentExtractor()
        parser.feed(html)
        output_text.insert(
            tk.END, f"--- HEADINGS ({len(parser.headings)}) ---\n"
        )
        for h in parser.headings[:20]:
            output_text.insert(tk.END, f"{h}\n")
        output_text.insert(
            tk.END, f"\n--- EXTERNAL LINKS ({len(parser.links)}) ---\n"
        )
        for link in set(parser.links[:25]):
            output_text.insert(tk.END, f"{link}\n")
    except Exception as e:
        messagebox.showerror("Scraping Failed", f"Error: {e}")


root = tk.Tk()
root.title("Web Page Content Scraper")
root.geometry("600x480")
tk.Label(
    root, text="WEB PAGE SCRAPER", font=("Arial", 16, "bold"), fg="#065f46"
).pack(pady=12)
input_frame = tk.Frame(root)
input_frame.pack(pady=5)
url_entry = tk.Entry(input_frame, width=45, font=("Arial", 10))
url_entry.pack(side="left", padx=5)
url_entry.insert(
    0, "https://en.wikipedia.org/wiki/Python_(programming_language)"
)
tk.Button(
    input_frame,
    text="Scrape",
    command=scrape_url,
    bg="#059669",
    fg="white",
    font=("Arial", 10, "bold"),
).pack(side="left")
output_text = tk.Text(root, height=18, width=68, wrap="word")
output_text.pack(padx=20, pady=15)
root.mainloop()
