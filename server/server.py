# Set up a simple client/server network
# Server setup

""""The `socket` module provides a low-level interface for network communication."""
import socket
"""serializing and deserializing ojects"""
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

# Define a class that allow to reuse the same data and
# switch between different formats more easily

class DataDeserializer:
    def __init__(self, data):
        self.data = data

    def deserialize_binary(self):
        return pickle.loads(self.data)

    def deserialize_json(self):
        return json.loads(self.data)

    def deserialize_xml(self):
        root = ET.fromstring(self.data)
        data_dict = {}
        for child in root:
            data_dict[child.tag] = child.text
        return data_dict


def Write_to_log(DATA):
    with open ("server/server_log.txt",'a') as file:
        file.write(str(DATA)+ '\n')


# Server setup
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'  # Server IP address (localhost in this case)
PORT = 1245  # Port to listen on

SERVER_SOCKET.bind((HOST, PORT))
SERVER_SOCKET.listen(1)  # Listen to one client at once

print(f"Server is listening on {HOST}:{PORT}")


while True:
    conn, addr = SERVER_SOCKET.accept()
    print(f"Connected by {addr}")
    
    FORMAT = conn.recv(1024).decode()
    RECIEVED_DATA = conn.recv(1024)
    deserilaizer = DataDeserializer (RECIEVED_DATA)
    while True:
        user_input1 = input("Print the received data on screen? (Y/N)").lower()
        user_input2 = input("Save the received data to log? (Y/N)").lower()
        if user_input1 == "y" and user_input2 == "y":
            Print_Screen = True
            Save_to_log = True
            break
        elif user_input1 =="n" and user_input2 == "n":
            Print_Screen = False
            Save_to_log = False
            break
        else:
            print("Error. Please try again")
    try:
        while True:
            if not FORMAT or not RECIEVED_DATA:
                break
            if FORMAT == "b":
                deserilazed_data = deserilaizer.deserialize_binary()
            elif FORMAT == "j":
                deserilazed_data = deserilaizer.deserialize_json()
            elif FORMAT == "x":
                deserilazed_data = deserilaizer.deserialize_xml()

            if Print_Screen:
                print(deserilazed_data)
            if Save_to_log:
                Write_to_log(deserilazed_data)

            break  #exit the loop after processing one set of data

        ENCRYPTED_OT_NOT = conn.recv(1024).decode()
        if not ENCRYPTED_OT_NOT:
            break
        elif ENCRYPTED_OT_NOT == "The text is encrypted." :
            print (ENCRYPTED_OT_NOT)
            key_message = conn.recv(2048)    
            if key_message:
                print ("Here is the key: ", key_message)
            else:
                break

            fernet = Fernet(key_message)
            # Receive the encrypted filename
            filename = conn.recv(1024).decode()  
            encrypted_text = conn.recv(1024).decode()
            if not filename or not encrypted_text:
                break
            decrypted_text = fernet.decrypt(encrypted_text).decode()
            with open (filename,'w') as recieved_file:
                recieved_file.write(decrypted_text)
            if Print_Screen:
                print(decrypted_text)
            if Save_to_log:
                Write_to_log(decrypted_text)
            break
        elif ENCRYPTED_OT_NOT == "The text is not encrypted.":
            print (ENCRYPTED_OT_NOT)
            filename = conn.recv(1024).decode()
            print(filename)
            file_text = conn.recv(1024)
            unpickled_text = pickle.loads(file_text)
            print(unpickled_text)
            if not filename or not file_text:
                break
            with open(filename, 'w') as create_file:
                create_file.write(unpickled_text)
            if Print_Screen:
                print(unpickled_text)
            if Save_to_log:
                Write_to_log(unpickled_text)
            break                
                
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        # Optionally, log the exception to a log file
        with open("server\error_log.txt", "a") as error_file:
            error_file.write(f"Exception: {str(e)}\n")

    conn.close()
    break

SERVER_SOCKET.close()