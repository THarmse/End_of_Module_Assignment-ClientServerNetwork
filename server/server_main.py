import json
from socket import socket, AF_INET, SOCK_STREAM
from common import decryption
from common.load_config import load_config


def server_main():
    """
    The main function for the server to handle incoming connections
    and decrypt data as needed.
    """

    # Load server configuration from YAML file
    config = load_config('server_config.yaml', caller='server')

    # Create a socket object with IPv4 and TCP/IP protocols
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Retrieve host and port details from config
    host = config['host']
    port = config['port']

    # Bind the socket to the given host and port
    server_socket.bind((host, port))

    # Enable the server to accept connections (up to 5 clients in the waiting queue)
    server_socket.listen(5)

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")

        # Receive data from the client (up to 4096 bytes)
        received_data = client_socket.recv(4096).decode('utf-8')

        # Parse the received JSON string into a Python dictionary
        parsed_data = json.loads(received_data)

        # Extract important fields from the received data
        encrypted_data = parsed_data['data']
        is_encrypted = parsed_data['isEncrypted']
        is_file = parsed_data['isFile']

        # If the data is encrypted, decrypt it
        if is_encrypted:
            decrypted_data = decryption.decrypt_data(encrypted_data.encode()).decode('utf-8')
        else:
            decrypted_data = encrypted_data

        print(f"Received data: {decrypted_data}, Encrypted: {is_encrypted}, Is File: {is_file}")

        # Close the client socket
        client_socket.close()


if __name__ == "__main__":
    server_main()
