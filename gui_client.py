import socket
import tkinter as tk
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def show_username_dialog():
    """Show a custom styled username dialog and return the entered username."""
    dialog = tk.Tk()
    dialog.title("Join Chat")
    dialog.geometry("360x240")
    dialog.resizable(False, False)
    dialog.configure(bg="#1e2024")

    dialog.update_idletasks()
    width = 360
    height = 240
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")

    username_var = tk.StringVar()
    result = {"username": None}

    def submit():
        username = username_var.get().strip()
        if not username:
            error_label.config(text="Username cannot be empty.")
            return
        if len(username) > 20:
            error_label.config(text="Username must be 20 characters or less.")
            return
        result["username"] = username
        dialog.destroy()

    def cancel():
        dialog.destroy()

    tk.Label(dialog, text="💬 Welcome to ChatApp",
             font=("Arial", 16, "bold"),
             fg="white", bg="#1e2024").pack(pady=(20, 8))

    tk.Label(dialog, text="Enter your username to join",
             font=("Arial", 10),
             fg="#b0b3b8", bg="#1e2024").pack(pady=(0, 15))

    entry = tk.Entry(dialog, textvariable=username_var,
                     font=("Arial", 12), justify="center",
                     bd=0, relief="flat", bg="#2b2d31", fg="white",
                     insertbackground="white", width=22)
    entry.pack(ipady=8, pady=(0, 8))
    entry.focus_set()

    error_label = tk.Label(dialog, text="",
                           font=("Arial", 9),
                           fg="#ff6b6b", bg="#1e2024")
    error_label.pack(pady=(0, 10))

    button_frame = tk.Frame(dialog, bg="#1e2024")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Join Chat", command=submit,
              font=("Arial", 10, "bold"), bg="#5865f2", fg="white",
              activebackground="#4752c4", activeforeground="white",
              relief="flat", bd=0, padx=20, pady=8,
              cursor="hand2").grid(row=0, column=0, padx=8)

    tk.Button(button_frame, text="Cancel", command=cancel,
              font=("Arial", 10, "bold"), bg="#d9534f", fg="white",
              activebackground="#c9302c", activeforeground="white",
              relief="flat", bd=0, padx=20, pady=8,
              cursor="hand2").grid(row=0, column=1, padx=8)

    dialog.bind("<Return>", lambda event: submit())
    dialog.bind("<Escape>", lambda event: cancel())

    dialog.mainloop()
    return result["username"]

USERNAME = show_username_dialog()

if not USERNAME:
    exit()

def get_user_color(username):
    colors = ["#e05555", "#e09a55", "#55e09a", "#559ae0", "#a055e0", "#e055c8", "#55e0d4", "#e0d455"]
    index = sum(ord(c) for c in username) % len(colors)
    return colors[index]

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
        if ":" in message:
            username, text = message.split(":", 1)
        else:
            username, text = "", message

        bubble = tk.Frame(row, bg="#2e3138", padx=10, pady=6)
        bubble.pack(side="left")

        tk.Label(bubble, text=username, bg="#2e3138",
                 fg=get_user_color(username),
                 font=("Helvetica", 12, "bold")).pack(anchor="w")

        tk.Label(bubble, text=text.strip(), bg="#2e3138", fg="#e8e9ec",
                 font=("Helvetica", 12), wraplength=300).pack(anchor="w")

    messages_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)

def send_message():
    message = entry.get().strip()
    if not message:
        return

    add_bubble(f"You: {message}", "self")
    entry.delete(0, "end")
    client_socket.sendall((message + "\n").encode("utf-8"))

def receive_messages():
    while True:
        try:
            data = client_socket.recv(4096).decode("utf-8")
            if data:
                messages = data.strip().split("\n")
                for message in messages:
                    message = message.strip()
                    if not message:
                        continue
                    if message.startswith("["):
                        root.after(0, add_bubble, message, "system")
                    else:
                        root.after(0, add_bubble, message, "other")
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
client_socket.sendall((USERNAME + "\n").encode("utf-8"))

root = tk.Tk()
root.title("ChatApp")
root.geometry("500x400")
root.configure(bg="#1e2024")

header = tk.Frame(root, bg="#16171a", height=50)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="💬  ChatApp", bg="#16171a", fg="#e8e9ec",
         font=("Helvetica", 14, "bold")).pack(side="left", padx=16)

tk.Label(header, text=f"● Connected as {USERNAME}", bg="#16171a", fg="#55e09a",
         font=("Helvetica", 10)).pack(side="right", padx=16)

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

def on_close():
    try:
        client_socket.close()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

tk.Button(bar, text="Leave", bg="#e05555", fg="white", relief="flat",
          font=("Helvetica", 11), padx=12, command=on_close).pack(side="right", padx=(0, 8))
tk.Button(bar, text="Send", bg="#4a90d9", fg="white", relief="flat",
          font=("Helvetica", 11), padx=12, command=send_message).pack(side="right", padx=(0, 8))

thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

root.mainloop()