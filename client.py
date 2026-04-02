import socket
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    username = input("Enter your username: ")
    client_socket.send(username.encode("utf-8"))
    time.sleep(0.1)
    while True:
        message = input("Enter a message: ")
        if message.lower() == "quit":
            break
        client_socket.send(message.encode("utf-8"))

    client_socket.close()

if __name__ == "__main__":
    main()