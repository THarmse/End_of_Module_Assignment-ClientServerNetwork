from cryptography.fernet import Fernet

def encrypt_data(data, key):
    """
    Encrypt data using Fernet symmetric encryption and return the encrypted data.

    :param data: The unencrypted data, as a bytes object.
    :param key: The encryption key, as a bytes object.
    :return: The encrypted data, as a bytes object.
    """
    f = Fernet(key)
    return f.encrypt(data)
