"""
CMPT 371 A3: Multi-Client Chat Server
Architecture: TCP sockets with multithreaded client handling
"""

import socket
import threading

# Server configuration 
HOST = "0.0.0.0" # bind to all interfaces so clients on the network can connect
PORT = 5000
BUFFER_SIZE = 1024

# Active client connections stored as (socket, username) pairs
clients = []

# chat_history holds the last MAX_HISTORY messages to send to new joiners
chat_history = []
MAX_HISTORY = 10

def broadcast(message, sender_socket):
    """
    Send a message to all connected clients except the sender
    sender_socket=None means send to everyone (used for leave messages)

    We track failed sends and remove those clients — this handles the case
    where a client disconnects without us knowing yet
    """

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
    """
    Send a message to one specific client
    Used for chat history and command responses
    """

    try:
        client_socket.send((message + "\n").encode("utf-8"))
    except:
        pass


def send_chat_history(client_socket):
    """
    Send the last MAX_HISTORY messages to a newly joined client
    """

    if not chat_history:
        return

    for old_message in chat_history:
        send_private_message(client_socket, old_message)


def handle_client(client_socket, client_address):
    """
    Runs in its own thread for each connected client
    Handles the full lifecycle: username handshake, message loop, and cleanup

    Thread Safety: each client has its own thread so they never block each other
    If one client hangs or crashes, all others continue unaffected
    """

    try:
        # The first message sent by the client is always their username
        username = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()
        clients.append((client_socket, username))

        print(f"{username} has joined")
        
        # Send history before announcing so it appears first in the chat
        send_chat_history(client_socket)
        send_private_message(client_socket, "[You joined the chat]")
        broadcast(f"[{username} has joined the chat]", client_socket)

        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE).decode("utf-8").strip()

                # Empty message means the client closed the connection cleanly
                if not message:
                    break

                # /users replies privately, not broadcast to room, return the current list of online users
                if message == "/users":
                    online_users = [user for sock, user in clients]
                    users_message = "[Online users: " + ", ".join(online_users) + "]"
                    send_private_message(client_socket, users_message)
                    continue
                
                # Regular message: format it, save to history, broadcast to others
                formatted_message = f"{username}: {message}"
                print(formatted_message)

                chat_history.append(formatted_message)
                if len(chat_history) > MAX_HISTORY:
                    chat_history.pop(0) # drop oldest to stay within the limit

                broadcast(formatted_message, client_socket)

            except:
                # Client force-closed or network error, exit the message loop
                break

    except:
        username = "Unknown User"

    # Remove disconnected client from the active connection list and notify others they left
    if (client_socket, username) in clients:
        clients.remove((client_socket, username))

    broadcast(f"[{username} has left the chat]", None)
    print(f"{username} has disconnected")

    try:
        client_socket.close()
    except:
        pass


def main():
    """
    Main server loop
    Accepts incoming TCP connections and spawns one thread per client
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        # Block until a client connects, then hand them off to a dedicated thread
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )
        thread.start()


if __name__ == "__main__":
    main()