import os
from common.common_utils import load_config
from socket import socket, AF_INET, SOCK_STREAM


def read_key_from_file(filename):
    """
    Read the encryption key from a file.

    Parameters:
        filename (str): The full path to the key file.

    Returns:
        bytes: The encryption key.
    """
    with open(filename, 'rb') as file:
        key = file.read()
    return key


def server_main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate up to the root directory
    root_dir = os.path.dirname(current_dir)

    # Load server configuration
    config = load_config('server_config.yaml', caller='server')

    # Prepare for decryption by reading the key
    key_file_path = os.path.join(root_dir, 'utils', 'key.key')
    decryption_key = read_key_from_file(key_file_path)

    # Create a socket object
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Get server details from config
    host = config['host']
    port = config['port']

    # Bind to the port
    server_socket.bind((host, port))

    # Queue up to 5 requests
    server_socket.listen(5)

    while True:
        # Establish a connection with the client.
        client_socket, addr = server_socket.accept()

        print(f"Got a connection from {addr}")

        encrypted_data = client_socket.recv(1024)

        # Testing - encryption to still be done
        decrypted_data = encrypted_data

        print(f"Received data: {decrypted_data}")

        client_socket.close()


if __name__ == "__main__":
    server_main()
