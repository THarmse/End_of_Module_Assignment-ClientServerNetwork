from flask import Flask, render_template, jsonify
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import json
import os
import base64
from common import decryption
from common.load_config import load_config

app = Flask(__name__)

# Store received messages
received_messages = []


def handle_received_data(data, is_encrypted, is_file, file_path):
    """
    Function to handle the received data for both console output and Flask display.

    Parameters:
    data: The received data.
    is_encrypted: Whether the data is encrypted or not.
    is_file: Whether the data is a file or not.
    file_path: The path to the file if the data is a file.
    """
    display_message = ""

    if is_file:
        # Handle file data
        base64_decoded_data = base64.b64decode(data)
        with open(file_path, "wb") as f:
            f.write(base64_decoded_data)

        absolute_file_path = os.path.abspath(file_path)

        if is_encrypted:
            decrypted_data = decryption.decrypt_data(base64_decoded_data).decode('utf-8')
            display_message += f"File Content (Decrypted for viewing): {decrypted_data}"
        else:
            # If the data is not encrypted, read it directly from the file
            with open(file_path, "r") as f:
                display_message += f"File Content: {f.read()}"

        display_message += f" - The Text File is saved at: {absolute_file_path}"

    else:
        # Handle non-file data
        if is_encrypted:
            decrypted_data = decryption.decrypt_data(data.encode()).decode('utf-8')
            display_message = f"Received data (Decrypted for viewing): {decrypted_data}"
        else:
            display_message = f"Received data: {data}"

    # Print to console
    print(display_message)

    # Add to Flask display
    received_messages.append(display_message)


# Existing server_main code with minor changes
def server_main():
    config = load_config('server_config.yaml', caller='server')
    server_socket = socket(AF_INET, SOCK_STREAM)
    host = config['host']
    port = config['port']
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")

        received_data = client_socket.recv(4096).decode('utf-8')
        parsed_data = json.loads(received_data)
        incoming_data = parsed_data['data']
        is_encrypted = parsed_data['isEncrypted']
        is_file = parsed_data['isFile']
        data_format = parsed_data['dataFormat']

        if not os.path.exists("server/text_files"):
            os.makedirs("server/text_files")

        file_path = "server/text_files/received_file.txt"

        handle_received_data(incoming_data, is_encrypted, is_file, file_path)

        client_socket.close()


@app.route('/')
def index():
    return render_template('index.html', messages=received_messages)


@app.route('/get_messages')
def get_messages():
    return jsonify(received_messages=received_messages)


@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    global received_messages
    received_messages.clear()
    return 'Messages cleared', 200


def run_flask_app():
    app.run(port=5001)


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()
    server_main()
