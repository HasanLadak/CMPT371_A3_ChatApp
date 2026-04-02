import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 1024

clients = []
chat_history = []
MAX_HISTORY = 10


def broadcast(message, sender_socket):
    dead_clients = []

    for client_socket, username in clients:
        if client_socket != sender_socket:
            try:
                client_socket.sendall((message + "\n").encode("utf-8"))
            except:
                dead_clients.append((client_socket, username))

    for dead_client in dead_clients:
        if dead_client in clients:
            clients.remove(dead_client)


def send_private_message(client_socket, message):
    try:
        client_socket.send((message + "\n").encode("utf-8"))
    except:
        pass


def send_chat_history(client_socket):
    if not chat_history:
        return

    for old_message in chat_history:
        send_private_message(client_socket, old_message)


def handle_client(client_socket, client_address):

    try:
        username = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        clients.append((client_socket, username))

        print(f"{username} has joined")
        send_chat_history(client_socket)
        broadcast(f"[{username} has joined the chat]", client_socket)

        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()

                if not message:
                    break

                if message == "/users":
                    online_users = [user for sock, user in clients]
                    users_message = "[Online users: " + ", ".join(online_users) + "]"
                    send_private_message(client_socket, users_message)
                    continue

                formatted_message = f"{username}: {message}"
                print(formatted_message)

                chat_history.append(formatted_message)
                if len(chat_history) > MAX_HISTORY:
                    chat_history.pop(0)

                broadcast(formatted_message, client_socket)

            except:
                break

    except:
        username = "Unknown User"

    if (client_socket, username) in clients:
        clients.remove((client_socket, username))

    broadcast(f"[{username} has left the chat]", None)
    print(f"{username} has disconnected")

    try:
        client_socket.close()
    except:
        pass


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        thread.start()


if __name__ == "__main__":
    main()