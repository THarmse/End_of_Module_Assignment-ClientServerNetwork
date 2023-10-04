import unittest
import json
from unittest.mock import patch, Mock
import base64
from client.client_app import app
import pickle
import xml.etree.ElementTree as ET

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_Json_without_encrypt_not_file(self):
    
        sample_data = {
            "data": {"key": "value"},
            "format": "JSON",    # Test JSON serialization
            "encrypt": False,
            "asTextFile": False
        }

        response = self.app.post('/send_data', json=sample_data)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected serialized data
        expected_data = json.dumps(sample_data['data'])
        self.assertEqual(response.json['data'], expected_data)

    def test_Binary_without_encrypt_not_file(self):
        # Prepare a sample JSON request with different serialize formats
        sample_data = {
            "data": {"key": "value"},
            "format": "Binary",    # Test JSON serialization
            "encrypt": False,
            "asTextFile": False
        }
        
        response = self.app.post('/send_data', json=sample_data)
        self.assertEqual(response.status_code, 200)

        # Deserialize the response data (base64 decode and unpickle)
        expected_data_bytes = base64.b64decode(response.json['data'].encode())
        expected_data = pickle.loads(expected_data_bytes)
        self.assertEqual(expected_data, sample_data['data'])

    def test_xml_no_encryption_no_file(self):
        # Prepare a sample request with XML data for XML serialization
        sample_data = {
            "data": {"key": "value"},
            "format": "XML",
            "encrypt": False,
            "asTextFile": False
        }

        response = self.app.post('/send_data', json=sample_data)
        self.assertEqual(response.status_code, 200)

        # Parse the response data as XML
        root = ET.fromstring(response.json['data'])

        # Check if the XML contains the correct data
        self.assertEqual(root.tag, 'root')
        items = list(root.iter('item'))
        self.assertEqual(len(items), 1)  # Ensure there is only one <item> element

        key_element = items[0].find('key')
        value_element = items[0].find('value')
        self.assertIsNotNone(key_element)
        self.assertIsNotNone(value_element)

        key_value = key_element.text
        value_text = value_element.text

        # Verify that the text content of XML elements matches the expected data
        self.assertEqual(key_value, "key")
        self.assertEqual(value_text, "value")
    
    @patch('client.client_app.encryption.encrypt_data')
    def test_json_encrypted_no_file(self,mock_encrypt_data):
        sample_data = {
            "data": {"key": "value"},
            "format": "Json",
            "encrypt": True,
            "asTextFile": False
        }

        # Mock the behavior of the encrypt_data function
        encrypted_data = b"encrypted_data"
        mock_encrypt_data.return_value = encrypted_data

        json_data = json.dumps(sample_data['data'])

        # Make an HTTP POST request to /send_data with the sample data
        response = self.app.post('/send_data', json=sample_data)

        # Assert the expected behavior or response
        self.assertEqual(response.status_code, 200)  # Expected status code

        # Ensure that the encrypt_data function is called with the correct arguments
        mock_encrypt_data.assert_called_once_with(json_data.encode())

        # Ensure that the response data matches the expected encrypted data
        expected_response_data = encrypted_data
        self.assertEqual(response.json['data'], encrypted_data)
   

if __name__ == '__main__':
    unittest.main()
