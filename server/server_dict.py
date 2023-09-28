"""serializing and deserializing ojects"""
import pickle
import json
import xml.etree.ElementTree as ET

# Define a class that allow to reuse the same data and
# switch between different formats more easily

class DataDeserializer:
    def __init__(self, data):
        self.data = data

    def serialize_binary(self):
        return pickle.loads(self.data).decode()

    def serialize_json(self):
        return json.loads(self.data)

    def serialize_xml(self):
        root = ET.fromstring(self.data)
        data_dict = {}
        for child in root:
            data_dict[child.tag] = child.text
        return data_dict


