import os


def create_temp_text_file(data):
    """
    Create a temporary text file and write the provided data into it.

    This function is utilized in the Flask application to create a text file
    from the serialized data. The created text file is saved in a folder named
    'text_files' in the current directory.

    Parameters:
    data (str): The serialized and optionally encrypted data to write into the text file.

    Returns:
    str: The absolute path of the created text file in 'text_files' directory.
    """

    # Create the 'text_files' directory if it doesn't exist
    if not os.path.exists('text_files'):
        os.makedirs('text_files')

    # Create a complete path for the new text file in 'text_files' directory
    temp_file_path = os.path.join('text_files', 'temp_serialized_data.txt')

    # Open and write data to the text file
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(data)

    return temp_file_path
