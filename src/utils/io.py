from src.config.setup import PROJECT_ROOT
from src.config.logging import logger 
from typing import Optional
from typing import Dict 
from typing import Any 
import json 
import yaml
import os


def load_api_key(file_path: str) -> str:
    """
    Loads the API key from a YAML file.

    Args:
        file_path (str): Path to the YAML file containing the API key.

    Returns:
        str: The API key.

    Raises:
        FileNotFoundError: If the credentials file is not found.
        ValueError: If the API key is missing in the YAML file.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
    try:
        logger.info("Loading API key from file.")
        with open(file_path, 'r') as file:
            credentials: Dict[str, Any] = yaml.safe_load(file)
        
        api_key: str = credentials.get("GOOGLE_API_KEY", "")
        if not api_key:
            raise ValueError("API key not found in the YAML file.")

        logger.info("API key successfully loaded.")
        return api_key

    except FileNotFoundError:
        logger.error(f"Credentials file not found at: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while loading API key: {e}")
        raise


def save_app_code(app_name_slug: str, frontend_code: str, backend_code: str) -> None:
    """
    Save the generated frontend and backend code to the appropriate location.

    Args:
        app_name_slug (str): The slugified app name.
        frontend_code (str): The frontend code as a string.
        backend_code (str): The backend code as a string.
    """
    apps_dir = os.path.join(PROJECT_ROOT, 'src', 'apps', app_name_slug)
    os.makedirs(apps_dir, exist_ok=True)

    frontend_path = os.path.join(apps_dir, 'frontend.py')
    backend_path = os.path.join(apps_dir, 'backend.py')

    try:
        with open(frontend_path, 'w', encoding='utf-8') as f:
            f.write(frontend_code)
        with open(backend_path, 'w', encoding='utf-8') as f:
            f.write(backend_code)
        logger.info("App code saved to: %s and %s", frontend_path, backend_path)
    except Exception as e:
        logger.error("Failed to save app code: %s", e)


def read_file(path: str) -> Optional[str]:
    """
    Reads the content of a markdown file and returns it as a text object.

    Args:
        path (str): The path to the markdown file.

    Returns:
        Optional[str]: The content of the file as a string, or None if the file could not be read.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content: str = file.read()
        return content
    except FileNotFoundError:
        logger.info(f"File not found: {path}")
        return None
    except Exception as e:
        logger.info(f"Error reading file: {e}")
        return None


def load_yaml(filename: str) -> Dict[str, Any]:
    """
    Load a YAML file and return its contents.

    Args:
        filename (str): The path to the YAML file.

    Returns:
        Dict[str, Any]: The parsed YAML object.

    Raises:
        FileNotFoundError: If the file is not found.
        yaml.YAMLError: If there is an error parsing the YAML file.
        Exception: For any other exceptions.
    """
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{filename}': {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading YAML file: {e}")
        raise


def load_json(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON file and return its contents.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON object, or None if an error occurs.

    Raises:
        FileNotFoundError: If the file is not found.
        json.JSONDecodeError: If there is an error parsing the JSON file.
        Exception: For any other exceptions.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"File '{filename}' contains invalid JSON.")
        return None
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise


def write_to_file(path: str, content: str) -> None:
    """
    Writes content to a specified file. Appends to the file if it already exists.

    Args:
        path (str): The path to the file.
        content (str): The content to write to the file.

    Raises:
        Exception: For any other exceptions encountered during file writing.
    """
    try:
        with open(path, 'a', encoding='utf-8') as file:
            file.write(content)
        logger.info(f"Content written to file: {path}")
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except Exception as e:
        logger.error(f"Error writing to file '{path}': {e}")
        raise
