# Set up a simple client/server network
# Set up Client

""""The `socket` module provides a low-level interface for network communication. """
import socket
"""serializing and deserializing ojects"""
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

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

#Crate a file
Text_to_file = input ("Pleae write someting to the file:")
with open ('client/new_file.txt','w') as file:
    file.write(Text_to_file)

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 1245

CLIENT_SOCKET.connect((HOST, PORT))

while True:
    #Serialize the data and send to the server
    FORMAT = input(
        "Choose a serialization format: B=Binary, J=Json, X=XML:").lower()

    if FORMAT == "b":
        serialized_binary = serializer.serialize_binary()
        CLIENT_SOCKET.send(FORMAT.encode())
        CLIENT_SOCKET.send(serialized_binary)
    elif FORMAT == "j":
        serialized_json = serializer.serialize_json()
        CLIENT_SOCKET.send(FORMAT.encode())
        CLIENT_SOCKET.send(serialized_json)
    elif FORMAT == "x":
        serialized_xml = serializer.serialize_xml()
        CLIENT_SOCKET.send(FORMAT.encode())
        CLIENT_SOCKET.send(serialized_xml)
    else:
        print("Error. Please try again.")

    #encrypted the text in file and sent it to the server
    
    while True:
        user_encrypt_or_not = input("Do you want to encrypt the text in file?(Y/N)")
        if user_encrypt_or_not == "y":
            encrypt_text = True
            CLIENT_SOCKET.send(b"The text is encrypted.")
            break
        elif user_encrypt_or_not == "n":
            encrypt_text = False
            CLIENT_SOCKET.send(b'The text is not encrypted.')
            break
        else:
            print("Error. Please try again.")

    if encrypt_text:
        # Key for encryption (keep this secret)
        key = Fernet.generate_key()
        print(key)
        fernet = Fernet(key)
        CLIENT_SOCKET.send(key)

         # Encrypt the text in the file
        with open('client/new_file.txt', 'rb') as encrypted_doc:
            encrypted_text = fernet.encrypt(encrypted_doc.read())
        #write a the encrypted text in to a file
        with open('client/encrypted_file.txt', 'wb') as file_to_send:
            file_to_send.write(encrypted_text)
        
        # Send the file name to server
        CLIENT_SOCKET.send(b"encrypted_file.txt")
        CLIENT_SOCKET.send(encrypted_text)
        
    else:
        CLIENT_SOCKET.send(b"new_file.txt")
        pickled_data = pickle.dumps(Text_to_file)
        CLIENT_SOCKET.send(pickled_data)
    break

CLIENT_SOCKET.close()
