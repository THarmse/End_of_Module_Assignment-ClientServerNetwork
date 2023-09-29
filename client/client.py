# Set up a simple client/server network
# Set up Client

""""The `socket` module provides a low-level interface for network communication. """
import socket
"""serializing and deserializing ojects"""
import pickle
import json
import xml.etree.ElementTree as ET

# Define a class that allow to reuse the same data and
# switch between serialization formats more easily

class DataSerializer:
    def __init__(self, data):
        self.data = data

    def serialize_binary(self):
        return pickle.dumps(self.data)

    def serialize_json(self):
        return json.dumps(self.data).encode()

    def serialize_xml(self):
        root = ET.Element("data")
        for key, value in self.data.items():
            child = ET.Element(key)
            child.text = str(value)
            root.append(child)
        return ET.tostring(root, encoding='utf-8')
    
# Creat a simple dictionary
MY_DICT = {
    'fruit': 'apple',
    'colour': 'red'
}
# serilze data
serializer = DataSerializer(MY_DICT)

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 1245

CLIENT_SOCKET.connect((HOST, PORT))

while True:
    FORMAT = input(
        "Choose a serialization format: B=Binary, J=Json, X=XML:").lower()

    if FORMAT == "b":
        serialized_binary = serializer.serialize_binary()
        CLIENT_SOCKET.send(FORMAT.encode())
        CLIENT_SOCKET.send(serialized_binary)
        break
    elif FORMAT == "j":
        serialized_json = serializer.serialize_json()
        CLIENT_SOCKET.send(FORMAT.encode())
        CLIENT_SOCKET.send(serialized_json)
        break
    elif FORMAT == "x":
        serialized_xml = serializer.serialize_xml()
        CLIENT_SOCKET.send(FORMAT.encode())
        CLIENT_SOCKET.send(serialized_xml)
        break
    else:
        print("Error. Please try again.")
    break


CLIENT_SOCKET.close()
