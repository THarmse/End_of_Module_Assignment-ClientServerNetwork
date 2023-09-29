import base64

from flask import Flask, request, jsonify, render_template, send_file
import json
import pickle
import xml.etree.ElementTree as ET

from client.utils.create_text_file import create_temp_text_file


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.json['data']
    serialize_format = request.json['format']
    encrypt = request.json['encrypt']
    as_text_file = request.json['asTextFile']

    if encrypt:
        data = ''.join(chr(ord(c) + 3) for c in json.dumps(data))

    serialized_data = ""
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

    if as_text_file:  # If Submit as Text file is selected
        temp_file_path = create_temp_text_file(serialized_data)
        print(temp_file_path)
        return send_file(temp_file_path, as_attachment=True, download_name="serialized_data.txt")

    return jsonify({"status": "success", "data": serialized_data}), 200

if __name__ == '__main__':
    app.run(debug=True)
