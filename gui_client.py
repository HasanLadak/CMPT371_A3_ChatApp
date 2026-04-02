import socket
import tkinter as tk
import threading
from tkinter import simpledialog

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

root_temp = tk.Tk()
root_temp.withdraw()
USERNAME = simpledialog.askstring("Username", "Enter your username:", parent=root_temp)
root_temp.destroy()

def add_bubble(message, bubble_type):
    row = tk.Frame(messages_frame, bg="#1e2024")
    row.pack(fill="x", padx=10, pady=2)

    if bubble_type == "system":
        tk.Label(row, text=message, bg="#1e2024", fg="#8b8fa8",
                 font=("Helvetica", 10)).pack()
    elif bubble_type == "self":
        bubble = tk.Frame(row, bg="#4a90d9", padx=10, pady=6)
        bubble.pack(side="right")
        tk.Label(bubble, text=message, bg="#4a90d9", fg="white",
                 font=("Helvetica", 12), wraplength=300).pack()
    else:
        bubble = tk.Frame(row, bg="#2e3138", padx=10, pady=6)
        bubble.pack(side="left")
        tk.Label(bubble, text=message, bg="#2e3138", fg="#e8e9ec",
                 font=("Helvetica", 12), wraplength=300).pack()

    messages_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)

def send_message():
    message = entry.get().strip()
    if not message:
        return

    add_bubble(f"You: {message}", "self")
    entry.delete(0, "end")
    client_socket.send(message.encode("utf-8"))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                if message.startswith("["):
                    root.after(0, add_bubble, message, "system")
                else:
                    root.after(0, add_bubble, message, "other")
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
client_socket.send(USERNAME.encode("utf-8"))

thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

root = tk.Tk()
root.title("ChatApp")
root.geometry("500x400")
root.configure(bg="#1e2024")

canvas = tk.Canvas(root, bg="#1e2024", bd=0, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(fill="both", expand=True)

messages_frame = tk.Frame(canvas, bg="#1e2024")
canvas_window = canvas.create_window((0, 0), window=messages_frame, anchor="nw")

canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

bar = tk.Frame(root, bg="#2a2d32")
bar.pack(fill="x", padx=10, pady=10)

entry = tk.Entry(bar, bg="#2a2d32", fg="#e8e9ec", font=("Helvetica", 12),
                 relief="flat", insertbackground="white")
entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)
entry.bind("<Return>", lambda e: send_message())

tk.Button(bar, text="Send", bg="#4a90d9", fg="white", relief="flat",
          font=("Helvetica", 11), padx=12, command=send_message).pack(side="right", padx=(0, 8))

root.mainloop()