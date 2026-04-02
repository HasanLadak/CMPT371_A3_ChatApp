import socket

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 1024

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        message = client_socket.recv(BUFFER_SIZE).decode("utf-8")
        username = message
        print(f"{username} has joined")

        while True:
            message = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            if not message:
                break
            print(f"{username}: {message}")

        print(f"{username} has disconnected")

        client_socket.close()

if __name__ == "__main__":
    main()