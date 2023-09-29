from cryptography.fernet import Fernet

def decrypt_data(data, key):
    """
    Decrypt data using Fernet symmetric encryption and return the decrypted data.

    :param data: The encrypted data, as a bytes object.
    :param key: The encryption key, as a bytes object.
    :return: The decrypted data, as a bytes object.
    """
    f = Fernet(key)
    return f.decrypt(data)
