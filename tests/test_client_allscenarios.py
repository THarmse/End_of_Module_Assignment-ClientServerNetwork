import unittest
import json
import base64
from unittest.mock import patch
from client.client_app import app
import tempfile


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client before each test."""
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        SEPARATOR = "-" * 80
        scenarios = [
            ("JSON", False, False, 200, "JSON"),
            ("JSON", False, True, 200, "JSON"),
            ("JSON", True, False, 200, "JSON"),
            ("JSON", True, True, 200, "JSON"),
            ("XML", False, False, 200, "XML"),
            ("XML", False, True, 200, "XML"),
            ("XML", True, False, 200, "XML"),
            ("XML", True, True, 200, "XML"),
            ("Binary", False, False, 200, "Binary"),
            ("Binary", False, True, 200, "Binary"),
            ("Binary", True, False, 200, "Binary"),
            ("Binary", True, True, 200, "Binary")
        ]

        for data_format, encrypt, as_text_file, _, expected_data_format in scenarios:
            with self.subTest(data_format=data_format, encrypt=encrypt, as_text_file=as_text_file):
                print(SEPARATOR)

                print(f"Testing scenario: Data format = {data_format}, Encrypt = {encrypt}, As text file = {as_text_file}")

                mock_encrypt_data.reset_mock()
                mock_create_temp_text_file.reset_mock()
                mock_socket.reset_mock()

                sample_data = {
                    "data": {"key1": "value1"},
                    "format": data_format,
                    "encrypt": encrypt,
                    "asTextFile": as_text_file
                }

                if data_format == "JSON":
                    data_content = json.dumps(sample_data['data']).encode()
                elif data_format == "XML":
                    data_content = b'<root><item><key>key1</key><value>value1</value></item></root>'
                else:
                    data_content = str(sample_data['data']).encode()

                mock_encrypt_data.return_value = b"encrypted_content" if encrypt else data_content

                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(data_content)
                    temp_file.flush()
                    temp_file_path = temp_file.name

                if as_text_file:
                    mock_create_temp_text_file.return_value = temp_file_path

                response = self.app.post('/send_data', json=sample_data)

                print(f"Expected status code: 200, Actual status code: {response.status_code}")
                self.assertEqual(response.status_code, 200)

                response_data = json.loads(response.data)
                print(f"Expected status: 'success', Actual status: {response_data['status']}")
                self.assertEqual(response_data['status'], 'success')

                if encrypt:
                    encrypted_data_bytes = b"encrypted_content"
                    mock_encrypt_data.return_value = encrypted_data_bytes
                else:
                    mock_encrypt_data.return_value = data_content

                if as_text_file:
                    mock_create_temp_text_file.assert_called_once()
                    with open(temp_file_path, "rb") as file:
                        file_content_bytes = file.read()
                        serialized_data = base64.b64encode(file_content_bytes).decode()

                    expected_server_data = {
                        'data': serialized_data,
                        'isEncrypted': encrypt,
                        'isFile': as_text_file,
                        'dataFormat': expected_data_format
                    }

                    mock_socket.return_value.send.assert_called_once_with(json.dumps(expected_server_data).encode())

                print()

        if __name__ == '__main__':
            unittest.main()
