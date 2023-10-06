# End_of_Module_Assignment-ClientServerNetwork
University of Liverpool - End of Module Assignment - Client Server Network - Repository

# Table of Contents
- [Installation](#installation)
- [How to run the project](#how-to-run-the-project)
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
3. Install dependencies from requirements.txt
```
pip install -r requirements.txt
```   
## How to run the project  
* Run on the same machine:  
  <br>
  Step 1  
  Open two terminals in the same machine  
  <br>
  Step 2  
  Navigate to the directory in both terminals  
  `cd End_of_Module_Assignment-ClientServerNetwork `  
  <br>
  Step 3  
  Run the server in terminal 1  
  `python -m server.server_main`  
  Click http://127.0.0.1:5001 to run the server on localhost  
  <br>
  Step 4  
  Run client in terminal 2  
  `python -m client.client_app`  
  Click http://127.0.0.1:5000 to run the client on localhost
  
* Run the project on different machines
  * Open the following links on a different machine  
    * https://livclient.naiva.co.za:5000/  
    * https://livserver.naiva.co.za:5001/

## Usage

Client
* Type in the data you want to send and click 'Add'
    - The entered data will be displayed on the screen, indicating a successful addition
* Choose the serialization format (JSON, Binary, or XML)
    - The serialized result will be displayed on the screen.
* Select whether to encrypt
* Chooses whether to send it as a file
* Click submit to send out the data  
* Submitted Successfully! will be displayed on the screen, indicating successful submission of data.  

Server  
* Configure the option to determine whether to save as a file.
  * Checking 'Switch to file' indicates saving the received data as a file
  * Not checking indicates print on the screen
* The 'Clear' Messages button is for deleting the history received data
* The 'Download Client Received File' button is for downloading files sent by the client.
* When in save as file mode: The 'Download All Received Messages File' button is for downloading all the received messages as file.

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
  - This test ensures that the `send_data` endpoint of the application behaves correctly.
  
- `test_server.py` - contains unit test for the server.
  - These tests verify the functionality of various endpoints in the server.
- To run all the unit tests for this project:  
  `python -m unittest`
  
## License
This project is open-source. (MIT License)

