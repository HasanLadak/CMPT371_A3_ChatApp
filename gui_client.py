import socket
import tkinter as tk
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
USERNAME = "Hadi"

def send_message():
    message = entry.get().strip()
    if not message:
        return

    chat_box.config(state="normal")
    chat_box.insert("end", f"You: {message}\n")
    chat_box.config(state="disabled")
    chat_box.yview("end")

    entry.delete(0, "end")

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.send(USERNAME.encode("utf-8"))
        time.sleep(0.1)
        client_socket.send(message.encode("utf-8"))
        client_socket.close()
    except Exception as e:
        chat_box.config(state="normal")
        chat_box.insert("end", f"[Error]: {e}\n")
        chat_box.config(state="disabled")

root = tk.Tk()
root.title("ChatApp")
root.geometry("500x400")
root.configure(bg="#1e2024")

chat_box = tk.Text(root, state="disabled", bg="#1e2024", fg="#e8e9ec",
                   font=("Helvetica", 12), relief="flat", padx=10, pady=10)
chat_box.pack(fill="both", expand=True, padx=10, pady=(10, 0))

bar = tk.Frame(root, bg="#2a2d32")
bar.pack(fill="x", padx=10, pady=10)

entry = tk.Entry(bar, bg="#2a2d32", fg="#e8e9ec", font=("Helvetica", 12),
                 relief="flat", insertbackground="white")
entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)
entry.bind("<Return>", lambda e: send_message())

tk.Button(bar, text="Send", bg="#4a90d9", fg="white", relief="flat",
          font=("Helvetica", 11), padx=12, command=send_message).pack(side="right", padx=(0, 8))

root.mainloop()