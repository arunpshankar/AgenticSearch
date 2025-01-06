from src.utils.io import load_api_key
from src.config.logging import logger 
from google import genai


def initialize_genai_client() -> genai.Client:
    """
    Initializes the GenAI client using the API key from a predefined credentials file.

    Returns:
        genai.Client: The initialized GenAI client.

    Raises:
        Exception: If the client initialization fails.
    """
    credentials_file = "./credentials/api.yml"

    try:
        logger.info("Loading API key from credentials file.")
        api_key = load_api_key(credentials_file)
        logger.info("Initializing GenAI client.")
        client = genai.Client(api_key=api_key)
        logger.info("GenAI client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GenAI client: {e}")
        raise