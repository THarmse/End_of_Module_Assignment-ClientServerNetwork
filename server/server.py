# Set up a simple client/server network
# Server setup

""""The `socket` module provides a low-level interface for network communication."""
import socket
"""serializing and deserializing ojects"""
import pickle
import json
import xml.etree.ElementTree as ET

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
    
def Print_Screen(user_input_for_print):
    if user_input_for_print == "y":
        return True
    elif user_input == "n":
        return False
    else:
        print("Error. Please try again.")
        return Print_Screen()

def Save_to_log(user_input_for_save):
    if user_input_for_save == "y":
        return True
    elif user_input == "n":
        return False
    else:
        print("Error. Please try again.")
        return Print_Screen()

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
        
        if FORMAT == "b":
            deserilazed_data = deserilaizer.deserialize_binary()
        elif FORMAT == "j":
            deserilazed_data = deserilaizer.deserialize_json()
        elif FORMAT == "x":
            deserilazed_data = deserilaizer.deserialize_xml()
        else:
            print("Error. Invalid format.")
            conn.close()
            break

        if Print_Screen(user_input1):
            print(deserilazed_data)
        if Save_to_log(user_input2):
            Write_to_log(deserilazed_data)

        break  #exit the loop after processing one set of data
    conn.close()
    break

SERVER_SOCKET.close()