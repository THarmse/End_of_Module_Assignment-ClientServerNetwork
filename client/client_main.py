import os
from common.load_config import load_config
from socket import socket, AF_INET, SOCK_STREAM

from common.encryption import encrypt_data


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


def client_main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate up to the root directory
    root_dir = os.path.dirname(current_dir)

    # Load client configuration
    config = load_config('client_config.yaml', caller='client')

    # Prepare for encryption by reading the key
    key_file_path = os.path.join(root_dir, 'utils', 'key.key')
    encryption_key = read_key_from_file(key_file_path)

    # Create a socket object
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Get client details from config
    host = config['server_host']
    port = config['server_port']

    # Establish a connection with the server
    client_socket.connect((host, port))

    # Prepare data
    data_to_send = "Hello, Liverpool!"

    # Testing of encrypted data to be done
    encrypted_data = data_to_send

    # Send encrypted data to server
    client_socket.send(encrypted_data.encode())

    # Close the socket
    client_socket.close()


if __name__ == "__main__":
    client_main()
