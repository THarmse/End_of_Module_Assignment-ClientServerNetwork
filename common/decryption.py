import os
from cryptography.fernet import Fernet


def read_key_from_file(filename):
    """
    Read the encryption key from a file.

    Parameters:
        filename (str): The full path to the key file.

    Returns:
        bytes: The encryption key.
    """
    with open(filename, 'rb') as file:
        key = file.read()
    return key


def decrypt_data(data):
    """
    Decrypt data using Fernet symmetric encryption and return the decrypted data.

    :param data: The encrypted data, as a bytes object.
    :return: The decrypted data, as a bytes object.
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate up to the root directory
    root_dir = os.path.dirname(current_dir)

    # Prepare for decryption by reading the key
    key_file_path = os.path.join(root_dir, 'utils', 'key.key')
    decryption_key = read_key_from_file(key_file_path)

    f = Fernet(decryption_key)

    return f.decrypt(data)
