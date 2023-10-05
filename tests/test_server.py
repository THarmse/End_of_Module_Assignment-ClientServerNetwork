import unittest

from common import decryption
from server.server_main import app, handle_received_data
import builtins
from unittest.mock import patch
import base64
import os


class ServerTestCase(unittest.TestCase):

    # Set up the testing environment
    def setUp(self):
        self.app = app.test_client()

    # send a GET request to the root URL '/' of the server, and check if the response
    # status code is 200, indicating a successful request
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # send a GET request to 'test_get_messages' and check if the response
    # status code is 200
    # Also check the response JSON data for the presence of('received_message',
    # 'file_or_print', 'file_path')
    def test_get_messages(self):
        response = self.app.get('/get_messages')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue('received_messages' in data)
        self.assertTrue('file_or_print' in data)
        self.assertTrue('file_path' in data)

    # Send a GET reuest to '/download_file', and check if the response
    # status code is 200
    def test_download_file(self):
        response = self.app.get('/download_file')
        self.assertEqual(response.status_code, 200)

    # Send a POST request to '/clear_messages', and check if the response
    # status code is 204 (successful request without a response body)
    def test_clear_messages(self):
        response = self.app.post('/clear_messages')
        self.assertEqual(response.status_code, 204)

    # Send a POST request to '/update_config' with JSON data contain the key
    # 'file_or_print' set to 'file' and check if the response status code is 200
    # also check the response JSON data for the presence of the key 'status' set to 'success'
    def test_update_config(self):
        data = {'file_or_print': 'file'}
        response = self.app.post('update_config', json=data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')

    def test_text_message(self):
        data = "Here it the test message."
        is_encrypted = False
        is_file = False
        file_path = 'test.txt'
        file_or_print = 'print'

        # Create a list to capture printed messages
        display_message = []

        # Create a mock print function to capture printed messages
        def mock_print(message):
            display_message.append(message)

        # Replace the original print function with the mock function
        original_print = builtins.print
        builtins.print = mock_print

        # Call the message handling function
        handle_received_data(data, is_encrypted, is_file, file_path, file_or_print)

        # Restore the original print function
        builtins.print = original_print

        # Check if the message is added to received_messages
        self.assertIn(f"Received data: {data}", display_message)

    def test_handle_received_data_encrypted_message(self):
        # Simulate receiving an encrypted message
        encrypted_data = "EncryptedMessage"
        is_encrypted = True
        is_file = False
        file_path = "test.txt"
        file_or_print = "print"

        # Create a list to capture printed messages
        display_messages = []

        # Create a mock print function to capture printed messages
        def mock_print(message):
            display_messages.append(message)

        # Replace the original print function with the mock function
        original_print = builtins.print
        builtins.print = mock_print

        # Mock the decrypt_data function to return a predefined value
        with patch("common.decryption.decrypt_data", return_value=b"DecryptedMessage"):
            # Call the message handling function inside the mock block
            handle_received_data(encrypted_data, is_encrypted, is_file, file_path, file_or_print)

        # Restore the original print function
        builtins.print = original_print

        # Check if the decrypted message is captured in printed_messages
        print(display_messages)
        self.assertIn(f"Received data (Decrypted for viewing): DecryptedMessage", display_messages)

    def test_encrypted_text_as_file(self):
        # Simulate receiving an encrypted file
        encrypted_data = "EncryptedMessage"
        send_as_file_data= base64.b64encode(encrypted_data.encode('utf-8'))
        is_encrypted = True
        is_file = True  # Set this to True to simulate receiving a file
        file_path = "test.txt"
        file_or_print = "print"

        # Create a list to capture printed messages
        display_messages = []

        # Create a mock print function to capture printed messages
        def mock_print(message):
            display_messages.append(message)

        # Replace the original print function with the mock function
        original_print = builtins.print
        builtins.print = mock_print

        # Mock the decrypt_data function to return a predefined value
        with patch("common.decryption.decrypt_data", return_value=b"DecryptedMessage"):
            # Call the message handling function inside the mock block
            handle_received_data(encrypted_data, is_encrypted, is_file, file_path, file_or_print)


        builtins.print = original_print
        actual_message = display_messages[0].strip()
        self.assertIn(f"File Content (Decrypted for viewing): DecryptedMessage", actual_message)



    def test_message_text_as_file (self):
        # Simulate receiving an encrypted file
        data = "Here is the data"
        received_data = base64.b64encode(data.encode())
        is_encrypted = False
        is_file = True
        file_path = "test.txt"
        file_or_print = "print"

        # Create a list to capture printed messages
        display_messages = []

        # Create a mock print function to capture printed messages
        def mock_print(message):
            display_messages.append(message)

        # Replace the original print function with the mock function
        original_print = builtins.print
        builtins.print = mock_print

        handle_received_data(received_data, is_encrypted, is_file, file_path, file_or_print)

        # Restore the original print function
        builtins.print = original_print

        actual_message = display_messages[0].strip()
        self.assertIn(f"File Content: {data}",  actual_message)

if __name__ == '__main__':
    unittest.main()
