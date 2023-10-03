import unittest
from server.server_main import app

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
    #Also check the response JSON data for the presence of('received_message'
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

if __name__ == '__main__':
    unittest.main()
