import base64
import json
import pickle
import socket
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, render_template, send_file
from client.utils.create_text_file import create_temp_text_file
from common import encryption
from common.load_config import load_config

# Initialize Flask application
app = Flask(__name__)


# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')


# Define the route for sending data
@app.route('/send_data', methods=['POST'])
def send_data():
    # Fetching data from client request
    data = request.json['data']
    serialize_format = request.json['format']
    encrypt = request.json['encrypt']
    as_text_file = request.json['asTextFile']

    # Initialize empty string to store serialized data
    serialized_data = ""

    # Serialize data based on the provided format
    if serialize_format == "JSON":
        serialized_data = json.dumps(data)
    elif serialize_format == "Binary":
        binary_data = pickle.dumps(data)
        serialized_data = base64.b64encode(binary_data).decode()
    elif serialize_format == "XML":
        root = ET.Element("root")
        for key, value in data.items():
            item = ET.SubElement(root, "item")
            ET.SubElement(item, "key").text = key
            ET.SubElement(item, "value").text = str(value)
        serialized_data = ET.tostring(root).decode()

    # Encrypt the data if encryption is selected
    if encrypt:
        # .decode() is used to convert bytes to string
        serialized_data = encryption.encrypt_data(serialized_data.encode()).decode()

    # Check if the user opted for file download
    if as_text_file:
        temp_file_path = create_temp_text_file(serialized_data)
        print(temp_file_path)
        return send_file(temp_file_path, as_attachment=True, download_name="serialized_data.txt")

    # Load server configurations
    config = load_config('client_config.yaml', caller='client')
    host = config['server_host']
    port = config['server_port']

    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Prepare data to send to server
    to_send = json.dumps({
        "data": serialized_data,
        "isEncrypted": encrypt,
        "isFile": as_text_file
    })

    # Send the data and close the socket
    client_socket.send(to_send.encode('utf-8'))
    client_socket.close()

    return jsonify({"status": "success", "data": serialized_data}), 200


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
