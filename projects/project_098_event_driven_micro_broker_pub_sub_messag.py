# Project 98: Event-Driven Micro-Broker & Pub/Sub Message Bus
# 100 Real-World Python Projects - Anuj Kumar Saxena
import queue
import threading
import time
import tkinter as tk


class MessageBroker:
    def __init__(self):
        self.topics = {}
        self.lock = threading.Lock()

    def subscribe(self, topic: str) -> queue.Queue:
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = []
            q = queue.Queue()
            self.topics[topic].append(q)
            return q

    def publish(self, topic: str, message: str):
        with self.lock:
            if topic in self.topics:
                for q in self.topics[topic]:
                    q.put(message)


broker = MessageBroker()
sub_queue = broker.subscribe("orders")


def consumer_loop():
    while True:
        msg = sub_queue.get()
        log_box.insert(tk.END, f"[RECEIVED] Topic 'orders' -> {msg}\n")
        log_box.see(tk.END)
        sub_queue.task_done()


threading.Thread(target=consumer_loop, daemon=True).start()


def emit_event():
    text = msg_entry.get().strip()
    if text:
        broker.publish("orders", text)
        msg_entry.delete(0, tk.END)


root = tk.Tk()
root.title("Pub/Sub Message Broker")
root.geometry("520x380")
tk.Label(
    root,
    text="EVENT-DRIVEN PUB/SUB BROKER",
    font=("Arial", 15, "bold"),
    fg="#1e3a8a",
).pack(pady=12)
f = tk.Frame(root)
f.pack(pady=6)
tk.Label(f, text="Publish to 'orders':").pack(side="left", padx=4)
msg_entry = tk.Entry(f, width=22)
msg_entry.pack(side="left", padx=4)
msg_entry.insert(0, "Order #4829 Created")
tk.Button(
    f,
    text="Publish Event",
    command=emit_event,
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left", padx=4)
log_box = tk.Text(
    root, height=11, width=58, font=("Consolas", 9), bg="#f8fafc"
)
log_box.pack(padx=20, pady=10)
root.mainloop()
