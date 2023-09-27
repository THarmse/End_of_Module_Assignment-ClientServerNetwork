# Set up a simple client/server network
# Server setup 

import socket

#Server setup
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1' #Server IP address (localhost in this case)
PORT = 1245 #Port to listen on

SERVER_SOCKET.bind((HOST,PORT))
SERVER_SOCKET.listen(1) #Listen to one client at once

print(f"Server is listening on {HOST}:{PORT}")