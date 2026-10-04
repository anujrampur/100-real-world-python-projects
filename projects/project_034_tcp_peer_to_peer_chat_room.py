# Project 34: TCP Peer-to-Peer Chat Room
# 100 Real-World Python Projects - Anuj Kumar Saxena
import socket
import threading
import tkinter as tk
from tkinter import messagebox

clients = []
server_socket = None
# --- CHAT CLIENT LOGIC ---
client_sock = None


def start_server():
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", 5555))
        server_socket.listen(5)
        srv_status.config(text="Server active on port 5555", fg="#15803d")
        btn_start_srv.config(state="disabled")

        def accept_clients():
            while True:
                sock, _ = server_socket.accept()
                clients.append(sock)
                threading.Thread(
                    target=handle_client, args=(sock,), daemon=True
                ).start()

        threading.Thread(target=accept_clients, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Server Error", f"{e}")


def broadcast(message, sender_sock=None):
    for c in list(clients):
        try:
            c.send(message.encode("utf-8"))
        except:
            clients.remove(c)


def handle_client(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if msg:
                broadcast(msg)
            else:
                break
        except:
            break
    if sock in clients:
        clients.remove(sock)
    sock.close()


# --- CLIENT UI INTERACTION ---
def connect_client():
    global client_sock
    nick = nick_entry.get().strip()
    if not nick:
        messagebox.showerror("Error", "Enter a nickname.")
        return
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(("127.0.0.1", 5555))
        client_sock.send(f"[{nick} joined the room]\n".encode("utf-8"))

        def receive_loop():
            while True:
                try:
                    data = client_sock.recv(1024).decode("utf-8")
                    if data:
                        chat_box.config(state="normal")
                        chat_box.insert(tk.END, data)
                        chat_box.config(state="disabled")
                        chat_box.see(tk.END)
                except:
                    break

        threading.Thread(target=receive_loop, daemon=True).start()
        btn_connect.config(state="disabled")
    except Exception as e:
        messagebox.showerror(
            "Connection Error", f"Unable to connect to server: {e}"
        )


def send_message():
    if not client_sock:
        return
    text = msg_entry.get().strip()
    nick = nick_entry.get().strip()
    if text:
        client_sock.send(f"{nick}: {text}\n".encode("utf-8"))
        msg_entry.delete(0, tk.END)


root = tk.Tk()
root.title("TCP Chat Suite")
root.geometry("500x520")
# Server control bar
srv_frame = tk.LabelFrame(root, text="Server Control", padx=10, pady=5)
srv_frame.pack(fill="x", padx=15, pady=5)
btn_start_srv = tk.Button(
    srv_frame,
    text="Start Local Server (5555)",
    command=start_server,
    bg="#0369a1",
    fg="white",
)
btn_start_srv.pack(side="left", padx=5)
srv_status = tk.Label(srv_frame, text="Server idle", fg="#64748b")
srv_status.pack(side="left", padx=10)
# Client area
c_frame = tk.Frame(root)
c_frame.pack(pady=5)
tk.Label(c_frame, text="Nickname:").pack(side="left", padx=2)
nick_entry = tk.Entry(c_frame, width=12)
nick_entry.pack(side="left", padx=4)
nick_entry.insert(0, "User1")
btn_connect = tk.Button(c_frame, text="Connect", command=connect_client)
btn_connect.pack(side="left", padx=4)
chat_box = tk.Text(root, height=16, width=55, state="disabled", bg="#f8fafc")
chat_box.pack(padx=15, pady=5)
send_frame = tk.Frame(root)
send_frame.pack(pady=5)
msg_entry = tk.Entry(send_frame, width=38)
msg_entry.pack(side="left", padx=4)
tk.Button(
    send_frame,
    text="Send",
    command=send_message,
    bg="#0284c7",
    fg="white",
    font=("Arial", 9, "bold"),
).pack(side="left")
root.bind("<Return>", lambda e: send_message())
root.mainloop()
