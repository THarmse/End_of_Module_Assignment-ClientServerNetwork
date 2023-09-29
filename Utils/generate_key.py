# generate_key.py

from cryptography.fernet import Fernet

def generate_key_to_file(filename="key.key"):
    """
    Generates an encryption key and saves it to a file. This is to be used by client and server.

    :param filename: The name of the file to save the encryption key in. Default is key.key
    """
    # Generate a new encryption key
    key = Fernet.generate_key()

    # Save the encryption key to a file
    with open(filename, "wb") as key_file:
        key_file.write(key)

if __name__ == "__main__":
    generate_key_to_file()
