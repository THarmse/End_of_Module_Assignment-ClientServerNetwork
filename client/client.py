# Set up a simple client/server network
# Set up Client

""""The `socket` module provides a low-level interface for network communication. """
import socket

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 1245

CLIENT_SOCKET.connect((HOST, PORT))
CLIENT_SOCKET.send(b'Hello')

CLIENT_SOCKET.close()
