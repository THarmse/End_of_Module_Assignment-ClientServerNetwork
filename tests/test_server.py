import unittest
import json
from unittest.mock import patch
from server.server_main import app


class MyTestCase(unittest.TestCase):
    
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('server_main.encryption.encrypt_data')
    #Mock the tncryotion funtion
    @patch('server_main.creat_temp_text_file')
    #Mock the text file creation function
    
    def test_send_data(self, mock_creat_temp_text_file,
                       mock_encrypt_data):
        
        sample_data ={
            "data" : {"key1":"value 1"},
            "format":"JSON",
            "encrypt": True,
            "asTextFile" : False
        } #Perpare a sample JSON request

        mock_encrypt_data.return_value = json.dumps(sample_data['data'])
        #Mock the behavior of the encrypt function

        mock_creat_temp_text_file.return_value = 'mock_file_path'
        #Mock the behavior of the text file creation function

        response = self.app.post('/send_data', json=sample_data)
        #Send a POST request to the /send_data route

        self.assertEqual(response.status_code,200)
        #Check if the response status code is 200(OK)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['status',"success"])
        #Check if the response contains a "status" filed with a
        #value of  "success"

        mock_encrypt_data.assert_called_once_with(json.dumps(sample_data['data']).encode())
        #Assert that the encrytion function was called with the correct arguments

        mock_creat_temp_text_file.assert_called_once_with()
        #Assert that the text file creation function was called since asTextFile is True

        expected_server_date ={
            'data':json.dumps(sample_data['data']),
            'isEncrypted': True,
            'isFile': True,
            'dataFormat':"JSON"
        }
        #Mock the expected data that should be sent ot the server

        mock_socket_send = mock_socket.socket().send
        with patch('socket.socket')as mock_socket:
            self.app.post('/send_data', json= sample_data)
            mock_socket_send.assert_call_once_with(json.dumps(expected_server_data).encode())
        #Check if the data sent to the server matches the expectations

if __name__ == '__main__':
    unittest.main()
