import os
import yaml


def load_config(config_file, caller=None):
    """
    Load a YAML configuration file to be used when hosting.
    This is re-usable and currently used by client and server.

    Parameters:
        config_file (str): The name of the config file.
        caller (str, optional): Indicates which module is calling the function.
                                Values can be 'client' or 'server'.

    Returns:
        dict: The loaded configuration as a dictionary.

    Raises:
        FileNotFoundError: If the specified config file is not found.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate up to the root directory assuming common remains as one level below root
    root_dir = os.path.dirname(current_dir)

    # Determine the folder where the config file is located based on the caller, i.e., Client or Server
    config_folder = os.path.join(root_dir, caller) if caller else root_dir

    # Construct the full path to the config file
    full_path = os.path.join(config_folder, 'config', config_file)

    try:
        with open(full_path, 'r') as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file {full_path} not found.") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}") from e
