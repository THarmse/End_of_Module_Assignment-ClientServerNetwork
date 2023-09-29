import base64
import json
import os
from socket import socket, AF_INET, SOCK_STREAM
from common import decryption
from common.load_config import load_config


def server_main():
    """
    The main function to handle incoming client connections and process
    received data according to server configurations.
    """

    # Load server configurations from a YAML file
    config = load_config('server_config.yaml', caller='server')

    # Create a socket object (IPv4 and TCP)
    server_socket = socket(AF_INET, SOCK_STREAM)

    # Retrieve host and port from the configuration
    host = config['host']
    port = config['port']

    # Bind the socket to the specified host and port
    server_socket.bind((host, port))

    # Set the server to listen for incoming connections
    server_socket.listen(5)

    while True:
        # Accept incoming connection
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")

        # Receive data from the client
        received_data = client_socket.recv(4096).decode('utf-8')

        # Deserialize the JSON string into a Python dictionary
        parsed_data = json.loads(received_data)

        # Extract relevant data fields
        incoming_data = parsed_data['data']
        is_encrypted = parsed_data['isEncrypted']
        is_file = parsed_data['isFile']

        # Create the 'server/text_files' directory if it doesn't exist
        if not os.path.exists("server/text_files"):
            os.makedirs("server/text_files")

        # Define the file path for saving received files inside the 'server/text_files' directory
        file_path = "server/text_files/received_file.txt"

        # Process received data based on whether it's a file or a simple message
        if is_file:
            # Decode the base64 encoded data
            base64_decoded_data = base64.b64decode(incoming_data)

            # Write the decoded data to a file
            with open(file_path, "wb") as f:
                f.write(base64_decoded_data)

            # Output the absolute file path
            absolute_file_path = os.path.abspath(file_path)
            print(f"File is saved at: {absolute_file_path}")

            # Decrypt the file content for display if it's encrypted
            if is_encrypted:
                decrypted_data = decryption.decrypt_data(base64_decoded_data).decode('utf-8')
                print(f"File Content (Decrypted for viewing): {decrypted_data}, Encrypted: {is_encrypted}, Is File: {is_file}")

            else:
                with open(file_path, "r") as f:
                    print(f"File Content: {f.read()}, Encrypted: {is_encrypted}, Is File: {is_file}")

        else:
            # Decrypt the message for display if it's encrypted
            if is_encrypted:
                decrypted_data = decryption.decrypt_data(incoming_data.encode()).decode('utf-8')
                print(f"Received data (Decrypted for viewing): {decrypted_data}, Encrypted: {is_encrypted}, Is File: {is_file}")

            else:
                print(f"Received data: {incoming_data}, Encrypted: {is_encrypted}, Is File: {is_file}")

        # Close the client socket connection
        client_socket.close()


if __name__ == "__main__":
    server_main()
