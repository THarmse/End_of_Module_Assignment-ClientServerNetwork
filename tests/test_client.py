import pickle
import unittest
import json
import base64
from unittest.mock import patch
from client.client_app import app
import tempfile
import xml.etree.ElementTree as ET
from common import encryption


class ClientTestCase(unittest.TestCase):

    def setUp(self):
        """Initialize test configuration.

        This method is run before each test. This is to set up a test client to
        mimic client-server interactions without starting an actual server.
        """
        app.config['TESTING'] = True
        self.app = app.test_client()

    # Helper function to drive different test scenarios for sending data
    def _test_send_data_scenario(self, data_format, encrypt, as_text_file, mock_socket,
                                 mock_create_temp_text_file, mock_encrypt_data):
        """Test a specific data sending scenario.

        This method performs the actual test logic for sending data of a given format
        (JSON, XML, Binary). Depending on the provided arguments, it prepares the data
        accordingly (e.g., encrypts it or converts it to the required format) and then
        tests whether the server received the data as expected.

        Args:
            data_format (str): Format of the data (e.g., "JSON", "XML", "Binary").
            encrypt (bool): Indicates whether the data should be encrypted.
            as_text_file (bool): Indicates whether the data should be sent as a text file.
            mock_socket: Mocked socket instance.
            mock_create_temp_text_file: Mocked tempfile creation function.
            mock_encrypt_data: Mocked data encryption function.
        """

        # Helper function to mock encryption. If `encrypt` is True, appends an empty byte sequence, otherwise returns data as-is.

        def mock_encryption_logic(data):
            return data + b"" if encrypt else data

        mock_encrypt_data.side_effect = mock_encryption_logic

        print("-" * 80)
        print(f"Testing scenario: Data format = {data_format}, Encrypt = {encrypt}, As text file = {as_text_file}")

        # Reset mocks for each scenario test
        mock_encrypt_data.reset_mock()
        mock_create_temp_text_file.reset_mock()
        mock_socket.reset_mock()

        # Define sample data based on the provided format and flags
        sample_data = {
            "data": {"key1": "value1"},
            "format": data_format,
            "encrypt": encrypt,
            "asTextFile": as_text_file
        }

        data_content = None
        if data_format == "JSON":
            data_content = json.dumps(sample_data['data'])
        elif data_format == "Binary":
            binary_data = pickle.dumps(sample_data['data'])
            data_content = base64.b64encode(binary_data).decode()
        elif data_format == "XML":
            root = ET.Element("root")
            for key, value in sample_data['data'].items():
                item = ET.SubElement(root, "item")
                ET.SubElement(item, "key").text = key
                ET.SubElement(item, "value").text = value
            data_content = ET.tostring(root, encoding='utf-8').decode()

        # Handling the as_text_file scenario
        if as_text_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(data_content.encode())
                temp_file.flush()
                temp_file_path = temp_file.name

            mock_create_temp_text_file.return_value = temp_file_path
        else:
            temp_file_path = None

        # Post data and verify the response
        response = self.app.post('/send_data', json=sample_data)
        print(f"Expected status code: 200, Actual status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        print(f"Expected status: 'success', Actual status: {response_data['status']}")
        self.assertEqual(response_data['status'], 'success')

        # Check if the data should be encrypted
        if encrypt:
            serialized_data = encryption.encrypt_data(data_content.encode()).decode()
        else:
            serialized_data = data_content if isinstance(data_content, str) else data_content.decode()

        # Check if data is sent as a file
        if as_text_file:
            mock_create_temp_text_file.assert_called_once()
            with open(temp_file_path, "rb") as file:
                file_content_bytes = file.read()
                serialized_data = base64.b64encode(file_content_bytes).decode()

        expected_server_data = {
            'data': serialized_data,
            'isEncrypted': encrypt,
            'isFile': as_text_file,
            'dataFormat': data_format
        }

        actual_server_data = json.loads(mock_socket.return_value.send.call_args[0][0].decode())

        print(f"Expected Server Data: {json.dumps(expected_server_data)}")
        print(f"Actual Server Data: {json.dumps(actual_server_data)}")
        self.assertEqual(expected_server_data, actual_server_data)

        mock_socket.return_value.send.assert_called_once_with(json.dumps(expected_server_data).encode())
        print()

    # Below are specific test scenarios for sending data, using the helper function above.

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_json_unencrypted_as_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending JSON format data without encryption and directly as data."""
        self._test_send_data_scenario("JSON", False, False, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_json_unencrypted_as_file(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending JSON format data without encryption but as a text file."""
        self._test_send_data_scenario("JSON", False, True, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_json_encrypted_as_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending JSON format data with encryption and directly as data."""
        self._test_send_data_scenario("JSON", True, False, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_json_encrypted_as_file(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending JSON format data with encryption and as a text file."""
        self._test_send_data_scenario("JSON", True, True, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_binary_unencrypted_as_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending Binary format data without encryption and directly as data."""
        self._test_send_data_scenario("Binary", False, False, mock_socket, mock_create_temp_text_file,
                                      mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_binary_unencrypted_as_file(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending Binary format data without encryption and as a text file."""
        self._test_send_data_scenario("Binary", False, True, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_binary_encrypted_as_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending Binary format data with encryption and directly as data."""
        self._test_send_data_scenario("Binary", True, False, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_binary_encrypted_as_file(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending Binary format data with encryption and as a text file."""
        self._test_send_data_scenario("Binary", True, True, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_xml_unencrypted_as_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending XML format data without encryption and directly as data."""
        self._test_send_data_scenario("XML", False, False, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_xml_unencrypted_as_file(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending XML format data without encryption and as a text file."""
        self._test_send_data_scenario("XML", False, True, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_xml_encrypted_as_data(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending XML format data with encryption and directly as data."""
        self._test_send_data_scenario("XML", True, False, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    @patch('client.client_app.encryption.encrypt_data')
    @patch('client.client_app.create_temp_text_file')
    @patch('socket.socket')
    def test_send_data_xml_encrypted_as_file(self, mock_socket, mock_create_temp_text_file, mock_encrypt_data):
        """Test sending XML format data with encryption and as a text file."""
        self._test_send_data_scenario("XML", True, True, mock_socket, mock_create_temp_text_file, mock_encrypt_data)

    if __name__ == '__main__':
        unittest.main()
