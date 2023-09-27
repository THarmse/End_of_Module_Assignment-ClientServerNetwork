# Set up a simple client/server network
# Set up Client

import socket

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 1245

CLIENT_SOCKET.connect((HOST,PORT)) 

