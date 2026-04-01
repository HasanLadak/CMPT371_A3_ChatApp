import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

    client_socket.close()

if __name__ == "__main__":
    main()