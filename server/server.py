# Set up a simple client/server network
# Server setup

""""The `socket` module provides a low-level interface for network communication."""
import socket

# Server setup
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'  # Server IP address (localhost in this case)
PORT = 1245  # Port to listen on

SERVER_SOCKET.bind((HOST, PORT))
SERVER_SOCKET.listen(1)  # Listen to one client at once

print(f"Server is listening on {HOST}:{PORT}")

while True:
    conn, addr = SERVER_SOCKET.accept()
    print(f"Connected by {addr}")
    DATA = conn.recv(1024)
    print("Recieved:",DATA.decode())

    conn.close()
    break

SERVER_SOCKET.close()