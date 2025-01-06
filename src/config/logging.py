import logging
import os


def custom_path_filter(path: str) -> str:
    """
    Filters the provided file path to shorten it by removing the project root portion.

    Parameters:
    -----------
    path : str
        The full file path to be filtered.

    Returns:
    --------
    str
        The shortened file path, with the project root removed if present.
    """
    project_root = "Agentic-Workflow-Patterns"
    
    # Find the index of the project root in the path
    idx = path.find(project_root)
    if idx != -1:
        # Extract the portion of the path after the project root
        path = path[idx + len(project_root):]
    return path

class CustomLogRecord(logging.LogRecord):
    """
    CustomLogRecord modifies the default LogRecord to filter and shorten the file path in log messages.
    
    Attributes:
    -----------
    pathname : str
        The full file path where the log message was generated, filtered to remove the project root.
    
    Methods:
    --------
    __init__(*args, **kwargs):
        Initializes the custom log record and applies the path filter.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pathname = custom_path_filter(self.pathname)

def setup_logger(log_filename: str = "app.log", log_dir: str = "logs") -> logging.Logger:
    """
    Sets up and configures the logger with custom log record handling and file/stream handlers.

    Parameters:
    -----------
    log_filename : str, optional
        The name of the log file, by default "app.log".
    log_dir : str, optional
        The directory where log files will be saved, by default "logs".

    Returns:
    --------
    logging.Logger
        The configured logger instance.
    """
    # Ensure the logging directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Define the log file path
    log_filepath = os.path.join(log_dir, log_filename)

    # Define the logging configuration
    logging.setLogRecordFactory(CustomLogRecord)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(module)s] [%(pathname)s]: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_filepath)
        ]
    )

    # Return the configured logger
    return logging.getLogger()


# Initialize the logger with the custom configuration.
logger = setup_logger()