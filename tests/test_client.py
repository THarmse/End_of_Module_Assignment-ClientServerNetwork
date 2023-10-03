import unittest
import json
import base64
from unittest.mock import patch
from client.client_app import app
import tempfile

class ClientTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('client_app.encryption.encrypt_data')
    # Mock the encryption function
    @patch('client_app.create_temp_text_file')
    # Mock the text file creation function
    @patch('socket.socket')
    
    def test_send_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        
        sample_data = {
            "data": {"key1": "value1"},
            "format": "JSON",
            "encrypt": True,
            "asTextFile": True
        }  # Prepare a sample JSON request

        mock_encrypt_data.return_value = json.dumps(sample_data['data'])
        # Mock the behavior of the encryption function

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b'file content')  # Write binary content to the temporary file
            temp_file.flush()  # Flush to ensure content is written
            temp_file_path = temp_file.name

        mock_create_temp_text_file.return_value = temp_file_path
        # Mock the behavior of the text file creation function

        response = self.app.post('/send_data', json=sample_data)
        # Send a POST request to the /send_data route

        self.assertEqual(response.status_code, 200)
        # Check if the response status code is 200 (OK)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        # Check if the response contains a "status" field with a
        # value of "success"

        mock_encrypt_data.assert_called_once_with(json.dumps(sample_data['data']).encode())
        # Assert that the encryption function was called with the correct arguments

        mock_create_temp_text_file.assert_called_once()
        # Assert that the text file creation function was called since asTextFile is True

        # Encode the file content as bytes and then base64 encode it
        with open(temp_file_path, "rb") as file:
            file_content_bytes = file.read()
            serialized_data = base64.b64encode(file_content_bytes).decode()

        expected_server_data = {
            'data': serialized_data,  # Use the base64 encoded content
            'isEncrypted': True,
            'isFile': True,
            'dataFormat': "JSON"
        }
        # Mock the expected data that should be sent to the server

        mock_socket_send = mock_socket.return_value.send
        with patch('socket.socket') as mock_socket:
            self.app.post('/send_data', json=sample_data)
            mock_socket_send.assert_called_once_with(json.dumps(expected_server_data).encode())
            # Check if the data sent to the server matches expectations

if __name__ == '__main__':
    unittest.main()
