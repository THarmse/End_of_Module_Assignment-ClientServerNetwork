import base64
import json
import pickle
import socket
import xml.etree.ElementTree as ET
from flask import Flask, request, jsonify, render_template
from client.utils.create_text_file import create_temp_text_file
from common import encryption
from common.load_config import load_config

# Initialize Flask application
app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the index page.
    """
    return render_template('index.html')


@app.route('/send_data', methods=['POST'])
def send_data():
    """
    Handle the data sent via POST request from the client.
    Serialize, encrypt, and forward the data to the server based on user choice.
    """
    # Fetch data and settings from the incoming JSON
    data = request.json['data']
    serialize_format = request.json['format']
    encrypt = request.json['encrypt']
    as_text_file = request.json['asTextFile']

    # Initialize a variable to store serialized data
    serialized_data = ""

    # Serialize the data based on the selected format
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

    # If encryption is selected, encrypt the serialized data
    if encrypt:
        serialized_data = encryption.encrypt_data(serialized_data.encode()).decode()

    # If the option for a text file is selected, write the serialized data into a text file
    if as_text_file:
        temp_file_path = create_temp_text_file(serialized_data)
        with open(temp_file_path, "rb") as file:
            file_content = file.read()
            serialized_data = base64.b64encode(file_content).decode()

    # Prepare the data for sending to the server
    to_send = json.dumps({
        "data": serialized_data,
        "isEncrypted": encrypt,
        "isFile": as_text_file
    })

    # Load server configurations and establish a socket connection
    config = load_config('client_config.yaml', caller='client')
    host = config['server_host']
    port = config['server_port']

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send the serialized data to the server
    client_socket.send(to_send.encode('utf-8'))

    # Close the client socket
    client_socket.close()

    return jsonify({"status": "success", "data": serialized_data}), 200


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
