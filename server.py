import socket
import threading

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 1024
clients = []

def broadcast(message, sender_socket):
    for client_socket, username in clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode("utf-8"))

def handle_client(client_socket, client_address):
    username = client_socket.recv(BUFFER_SIZE).decode("utf-8")
    clients.append((client_socket, username))
    broadcast(f"[{username} has joined the chat]", client_socket)
    print(f"{username} has joined")

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if not message:
                break
            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client_socket)
        except:
            break

    clients.remove((client_socket, username))
    broadcast(f"[{username} has left the chat]", None)
    print(f"{username} has disconnected")
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start() 

if __name__ == "__main__":
    main()