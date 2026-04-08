# CMPT 371 Assignment 3 - Multi-Client Chat Application

## Team Members
- Muhammad Hasan Ladak - 301589958 - mhl41@sfu.ca
- Muhammad Hadi Ladak - 301589952 - mhl40@sfu.ca

## 1. Project Overview & Description
A real-time multi-client chat application built using Python's TCP socket API and tkinter for the GUI.
The application follows a client-server architecture where a central server manages all connected clients and routes messages between them.
We also enhanced the system by adding TLS encryption to secure communication between clients and the server.

**Features**
- Multiple clients can connect and chat simultaneously
- Chat history is sent to newly joined clients
- `/users` command to see who is currently online
- Duplicate username detection
- Custom dark-themed GUI
- Message bubbles and user-specific colors
- Join and leave notifications
- Scrollable chat interface
- TLS encryption for secure client-server communication

## 2. System Limitations & Edge Cases

**Handling Multiple Clients Concurrently:**

Solution: We used Python’s threading module. Each client connection is handled in a separate thread, allowing multiple users to chat simultaneously.

Limitation: Thread creation depends on system resources. This approach is not scalable for very large numbers of users. A production system would use asynchronous I/O or thread pools.

**TCP Stream Buffering:**

Solution: Since TCP is a continuous byte stream, multiple messages can arrive combined. To handle this, we append a newline character `\n` to each message and split incoming data using this delimiter.

Limitation: Extremely large messages could theoretically still be split across two `recv()` calls. A full solution would require a persistent buffer, but for our use case the newline delimiter works reliably.

**Encrypted Communication (TLS):**

We implemented TLS (Transport Layer Security) to encrypt communication between the client and server. This ensures that all messages are encrypted in transit and cannot be easily intercepted on the network.

Limitation: This is not end-to-end encryption, as the server can still read and forward all messages and we use a self-signed certificate with certificate verification disabled for local testing.

**Chat History Handling:**

Solution: We store recent messages on the server and send them to newly connected users so they can see previous conversation context.

Limitation: The chat history is stored only in memory and is lost when the server restarts.

## 3. Video Demo
- [Watch Project Demo on Youtube](https://www.youtube.com/watch?v=z33Jbg3slIs)

## 4. Prerequisites (Fresh Environment)
To run our application, you need:

- Python 3.x
- No external libraries required - uses Python standard library only (`socket`, `ssl`, `threading`, `tkinter`)
- `server.crt` and `server.key` are included in the repo - no setup needed

## 5. Step-by-Step Run Guide

### Step 1: Clone the repository
```bash
git clone https://github.com/HasanLadak/CMPT371_A3_ChatApp.git
cd CMPT371_A3_ChatApp
```

### Step 2: Start the server
Open a terminal and run:
```bash
python server.py
```

You should see:
```
TLS server is listening on 0.0.0.0:5000
```
Keep this terminal open. Our server must be running before any clients connect.

### Step 3: Start a client
Open a **new terminal** and run:
```bash
python gui_client.py
```
Our username dialog will appear. Enter a username and click **Join Chat** or press **Enter**.

### Step 4: Connect more clients
Repeat Step 3 in additional terminal windows to simulate multiple users chatting at once.

### Step 5: Start chatting
Type messages and press **Enter** or click **Send**

Use `/users` to see currently connected users

Open multiple clients to simulate multiple users chatting together

## 6. Technical Protocol Details

We built a simple newline-delimited protocol on top of TCP to handle message framing.

### Framing
Since TCP is a byte stream with no natural message boundaries, we append `\n` to every message we send. The receiver buffers incoming data and splits on `\n` to extract complete messages.

Raw TCP stream:
"Hasan: hello\n[Hadi has joined the chat]\n"

After splitting on `\n`:
["Hasan: hello", "[Hadi has joined the chat]"]

### Message Types
The client distinguishes message types by checking if the message starts with `[`.

| Type   | Format           | Example                          | Rendered As              |
|--------|------------------|----------------------------------|--------------------------|
| Chat   | `username: text` | `Hasan: hey`                     | Colored chat bubble      |
| System | `[event text]`   | `[Hasan has joined the chat]`    | Grey centered text       |

### Message Flow

Client → Server:
- `username\n` → initial connection  
- `hello\n` → chat message  
- `/users\n` → command  

Server → Client:
- chat history (last 10 messages)  
- `[You joined]` (private)  
- `[username joined]` (broadcast)  
- `username: hello` (broadcast)  
- `[Online users: ...]` (private response) 

### Encryption

All communication is encrypted using TLS. The server wraps each accepted connection with `context.wrap_socket()` using a self-signed certificate. The client wraps its socket with `ssl.create_default_context()` before connecting. Certificate verification is disabled on the client side since we use a self-signed cert.

## 7. Academic Integrity & References

**Code Origin:**
- We implemented the core application ourselves including the server architecture, multi-threading, client-server communication, and chat protocol.

**GenAI Usage:**
- We used Claude to assist with the tkinter GUI frontend design and to help with concepts for TLS encryption. 

**References:**
- [Python Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
- [Real Python: Intro to Python Threading](https://realpython.com/intro-to-python-threading/)