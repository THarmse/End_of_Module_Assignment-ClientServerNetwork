import unittest
from server_main import app, handle_received_data
import base64

class ServerTestCase(unittest.TestCase):
    
    #Set up the testing enviroment
    def setUp(self):
        self.app = app.test_client()

    #send a GET request to the root URL '/' of the server, and check if the response 
    #status code is 200, indicating a successful request
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    #send a GET request to 'test_get_messages' and chcek if the response
    #status code is 200
    #Also check the response JSON data for the presence of('received_message',
    # 'file_or_print', 'file_path')
    def test_get_messages(self):
        response = self.app.get('/get_messages')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue('received_messages'in data)
        self.assertTrue('file_or_print' in data)
        self.assertTrue('file_path'in data)

    #Send a GET reuest to '/download_file', and check if the response
    #status code is 200
    def test_download_file(self):
        response = self.app.get('/download_file')
        self.assertEqual(response.status_code, 200)
    
    #Send a POST request to '/clear_messages', and check if the response
    #status code is 204 (successful request without a response body)
    def test_clear_messages(self):
        response = self.app.post('/clear_messages')
        self.assertEqual(response.status_code, 204)
    
    #Send a POST request to '/update_config' with JSON data contain the key
    #'file_or_print' set to 'file' and check if the response status code is 200
    #alsi check the response JSON data for the presence of the key 'status' set to 'success'
    def test_update_config(self):
        data = {'file_or_print':'file'}
        response = self.app.post('update_config',json =data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'],'success')

    def test_handle_received_data_text_message(self):
        data = "Here it the test message."
        is_encrypted = False
        is_file = False
        file_path = 'test.txt'
        file_or_print = 'print'

        display_message = []

        def mock_print (message):
            display_message.append(message)

        original_print = __builtins__.print
        __builtins__.print = mock_print

        handle_received_data(data, is_encrypted, is_file, file_path, file_or_print)

        __builtins__.print = original_print

        self.assertIn(f"Received data: {data}", display_message)

        def test_handle_received_data_encrypted_message(self):
        # Simulate receiving an encrypted message
            encrypted_data = "Base64EncodedEncryptedData"
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
            original_print = __builtins__.print
            __builtins__.print = mock_print

            # Call the message handling function
            handle_received_data(encrypted_data, is_encrypted, is_file, file_path, file_or_print)

            # Restore the original print function
            __builtins__.print = original_print

            # Check if the decrypted message is captured in printed_messages
            self.assertIn(f"Received data (Decrypted for viewing): DecryptedMessageHere", display_messages)
    

if __name__ == '__main__':
    unittest.main()
