import os
import tempfile


def create_temp_text_file(data):
    """
    Create a temporary text file and write the provided data into it.

    This function is utilized in the Flask application to create a text file
    from the serialized data, and downloading it to the user's windows temp folder.

    Parameters:
    data (str): The serialized and optionally encrypted data to write into the text file.

    Returns:
    str: The absolute path of the created temporary text file.
    """

    # Get the directory path for temporary files
    temp_dir = tempfile.gettempdir()

    # Create a complete path for the new temporary text file
    temp_file_path = os.path.join(temp_dir, "temp_serialized_data.txt")

    # Open and write data to the temporary text file
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(data)

    return temp_file_path
