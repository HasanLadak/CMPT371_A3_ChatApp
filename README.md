# CMPT 371 Assignment 3 - Multi-Client Chat Application

## Team Members
- Muhammad Hasan Ladak - 301589958 - mhl41@sfu.ca
- Muhammad Hadi Ladak - 301589952 - mhl40@sfu.ca

## 1. Project Overview & Description
A real-time multi-client chat application built using Python's TCP socket API and tkinter for the GUI.
The application follows a client-server architecture where a central server manages all connected clients and routes messages between them.

**Features**
- Multiple clients can connect and chat simultaneously
- Chat history is sent to newly joined clients
- `/users` command to see who is currently online
- Duplicate username detection
- Custom dark-themed GUI
- Message bubbles and user-specific colors
- Join and leave notifications
- Scrollable chat interface

## 2. System Limitations & Edge Cases

**Handling Multiple Clients Concurrently:**

Solution: We used Python’s threading module. Each client connection is handled in a separate thread, allowing multiple users to chat simultaneously.

Limitation: Thread creation depends on system resources. This approach is not scalable for very large numbers of users. A production system would use asynchronous I/O or thread pools.

**TCP Stream Buffering:**

Solution: Since TCP is a continuous byte stream, multiple messages can arrive combined. To handle this, we append a newline character `\n` to each message and split incoming data using this delimiter.

Limitation: Extremely large messages could theoretically still be split across two `recv()` calls. A full solution would require a persistent buffer, but for our use case the newline delimiter works reliably.

**No Message Encryption:**

We did not implement any encryption (e.g. TLS) in our application. Messages are sent as plain text over TCP, so this chat app should not be used for sensitive communication.

**Chat History Handling:**

Solution: We store recent messages on the server and send them to newly connected users so they can see previous conversation context.

Limitation: The chat history is stored only in memory and is lost when the server restarts.

## 3. Video Demo
- Link to be added

## 4. Prerequisites (Fresh Environment)
To run our application, you need:

- Python 3.x
- No external libraries required - uses Python standard library only (`socket`, `threading`, `tkinter`)

## 5. Step-by-Step Run Guide

### Step 1: Clone the repository
```bash
git clone https://github.com/YOURUSERNAME/CMPT371_A3_ChatApp.git
cd CMPT371_A3_ChatApp
```

### Step 2: Start the server
Open a terminal and run:
```bash
python server.py
```

You should see:
```
Server is listening on 0.0.0.0:5000
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