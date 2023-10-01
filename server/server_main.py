from flask import Flask, render_template, jsonify, send_file, request
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import json
import os
import base64
import yaml
from yaml.representer import SafeRepresenter
from common import decryption
from common.load_config import load_config
from pathlib import Path


# Custom representer to always quote strings as the flask app will replace the config
def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


# Add the custom string presenter
SafeRepresenter.add_representer(str, quoted_presenter)

app = Flask(__name__)

# Store received messages
received_messages = []

# Load configuration settings from server_config.yaml
config = load_config('server_config.yaml', caller='server')
file_or_print = None
root_dir = os.path.dirname(os.path.abspath(__file__))
received_file_path = os.path.join(root_dir, config.get('received_file_path').replace("/", os.sep))
all_messages_received_path = os.path.join(root_dir, config.get('all_messages_received_path').replace("/", os.sep))


def handle_received_data(data, is_encrypted, is_file, file_path, file_or_print):
    """
    Handles received data and writes to either console or file depending on configuration.

    Parameters:
    data (str): The data received from the client.
    is_encrypted (bool): Indicates whether the data is encrypted.
    is_file (bool): Indicates whether the received data is a file.
    file_path (str): The path to save the received file, if it is a file.
    file_or_print (str): Configuration to either display data on the console or write to a file.
    """
    display_message = ""

    if is_file:
        base64_decoded_data = base64.b64decode(data)
        with open(file_path, "wb") as f:
            f.write(base64_decoded_data)

        absolute_file_path = Path(file_path).resolve()

        if is_encrypted:
            decrypted_data = decryption.decrypt_data(base64_decoded_data).decode('utf-8')
            display_message += f"File Content (Decrypted for viewing): {decrypted_data}"
        else:
            with open(file_path, "r") as f:
                display_message += f"File Content: {f.read()}"

        display_message += f" - The Text File is saved at: {absolute_file_path}"

    else:
        if is_encrypted:
            decrypted_data = decryption.decrypt_data(data.encode()).decode('utf-8')
            display_message = f"Received data (Decrypted for viewing): {decrypted_data}"
        else:
            display_message = f"Received data: {data}"

    if file_or_print == "file":
        with open(all_messages_received_path, "a") as f:
            f.write(display_message + "\n")
    else:
        print(display_message)
        received_messages.append(display_message)


def server_main():
    """
    Main function to run the server.
    """
    # Server settings
    config = load_config('server_config.yaml', caller='server')
    global file_or_print  # Declare global variable for updates
    host = config['host']
    port = config['port']

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        config = load_config('server_config.yaml', caller='server')
        file_or_print = config.get('file_or_print_display')

        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")

        received_data = client_socket.recv(4096).decode('utf-8')
        parsed_data = json.loads(received_data)

        incoming_data = parsed_data['data']
        is_encrypted = parsed_data['isEncrypted']
        is_file = parsed_data['isFile']

        if not os.path.exists("text_files"):
            os.makedirs("text_files")

        handle_received_data(incoming_data, is_encrypted, is_file, received_file_path, file_or_print)

        client_socket.close()


@app.route('/')
def index():
    return render_template('index.html', messages=received_messages)


@app.route('/get_messages')
def get_messages():
    return jsonify(received_messages=received_messages, file_or_print=file_or_print,
                   file_path=os.path.abspath(all_messages_received_path))


@app.route('/clearButton')
def download_file():
    return send_file(all_messages_received_path, as_attachment=True)


@app.route('/download_client_file')
def download_client_file():
    return send_file(received_file_path, as_attachment=True)


@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    global received_messages

    if file_or_print == 'print':
        received_messages.clear()
    elif file_or_print == 'file':
        with open(all_messages_received_path, 'w') as f:
            f.write('')

    return '', 204


@app.route('/update_config', methods=['POST'])
def update_config():
    global file_or_print  # Declare global variable for updates

    data = request.json
    new_value = data.get('file_or_print')

    try:
        # Load the current config using load_config function
        config_data = load_config('server_config.yaml', caller='server')

        # Update the value in the loaded config
        config_data['file_or_print_display'] = new_value

        # Get the directory path for the config file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        config_folder = os.path.join(root_dir, 'server', 'config')
        full_path = os.path.join(config_folder, 'server_config.yaml')

        # Save the updated config back to the file
        with open(full_path, 'w') as f:
            yaml.safe_dump(config_data, f, default_flow_style=False)

        file_or_print = new_value
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'failed', 'error': str(e)})


def run_flask_app():
    app.run(host='0.0.0.0', port=5001)


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()
    server_main()
