# End_of_Module_Assignment-ClientServerNetwork
University of Liverpool - End of Module Assignment - Client Server Network - Repository

# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Unit test](#unit-test)
- [License](#license)

SecureFile
https://pypi.org/project/securefile/
type `pip install securefile` to install this package in native python  
## Installation

1. Clone the repository using the following command  
```
git clone https://github.com/THarmse/End_of_Module_Assignment-ClientServerNetwork.git
```     
2. Navigate to the directory
```
cd End_of_Module_Assignment-ClientServerNetwork  
```  
3. Install dependencies from requirement.txt
```
pip install -r requirement.txt
```   

## Usage

https://livclient.naiva.co.za:5000/
https://livserver.naiva.co.za:5001/

## Directory Structure

nd_of_Module_Assignment-ClientServerNetwork/  
┣ client/  
┃ ┣ config/  
┃ ┃ ┗ client_config.yaml  
┃ ┣ static/  
┃ ┃ ┣ images/  
┃ ┃ ┃ ┗ University_of_Liverpool.jpg  
┃ ┃ ┣ main.js  
┃ ┃ ┗ styles.css  
┃ ┣ templates/  
┃ ┃ ┗ index.html  
┃ ┣ text_files/  
┃ ┃ ┗ temp_serialized_data.txt  
┃ ┣ utils/  
┃ ┃ ┗ create_text_file.py  
┃ ┣ client_app.py  
┃ ┗ __init__.py  
┣ common/  
┃ ┣ decryption.py  
┃ ┣ encryption.py  
┃ ┗ load_config.py  
┣ server/  
┃ ┣ config/  
┃ ┃ ┗ server_config.yaml  
┃ ┣ static/  
┃ ┃ ┣ images/  
┃ ┃ ┃ ┗ University_of_Liverpool.jpg  
┃ ┃ ┣ main.js  
┃ ┃ ┗ styles.css  
┃ ┣ templates/  
┃ ┃ ┗ index.html  
┃ ┣ text_files/  
┃ ┃ ┣ all_messages_received.txt  
┃ ┃ ┗ received_file.txt  
┃ ┣ server_main.py  
┃ ┗ __init__.py  
┣ tests/  
┃ ┣ test_client.py  
┃ ┣ test_server.py  
┃ ┗ __init__.py  
┣ text_files/  
┣ utils/  
┃ ┣ generate_key.py  
┃ ┗ key.key  
┣ Commands.txt  
┣ LICENSE  
┣ README.md  
┗ requirements.txt  

## Unit test
- `test_client.py` - contains unit test for the client app.  
  This test ensures that the `send_data` endpoint of the application behaves correctly.
- `test_server.py` - contains unit test for the server.  
  These tests verify the functionality of various endpoints in the server.
  
## License
This project is open-source. (MIT License)

