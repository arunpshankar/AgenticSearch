from src.config.logging import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os


# Configuration Constants
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(os.path.dirname(BASE_DIR))
DATA_DIR: str = os.path.join(PROJECT_ROOT, 'data')
DB_DIR: str = os.path.join(PROJECT_ROOT, 'db')
DB_PATH: str = os.path.join(DB_DIR, 'apis.db')
CSV_PATH: str = os.path.join(DATA_DIR, 'apis.csv')
IMAGES_DIR: str = os.path.join(PROJECT_ROOT, 'img')
GOOGLE_ICON_PATH: str = os.path.join(IMAGES_DIR, 'google_logo.svg')
TEMPLATES_DIR: str = os.path.join(PROJECT_ROOT, 'templates')

# Global Engine variable
engine: Engine

def setup_directories() -> None:
    """
    Create necessary directories for the project.
    Ensures `db` and `data` directories exist.
    Logs any issues during directory creation.
    """
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        logger.info(f"Directories ensured: {DB_DIR}, {DATA_DIR}")
    except OSError as e:
        logger.error(f"Error creating directories: {e}")
        raise


def initialize_database(db_path: str) -> Engine:
    """
    Initialize a SQLite database using SQLAlchemy.

    Args:
        db_path (str): Path to the SQLite database file.

    Returns:
        Engine: SQLAlchemy database engine.
    
    Logs database initialization status.
    """
    try:
        engine = create_engine(f'sqlite:///{db_path}', echo=False)
        logger.info(f"Database initialized at {db_path}")
        return engine
    except Exception as e:
        logger.error(f"Failed to initialize database at {db_path}: {e}")
        raise

# Setup happens when the module is imported
try:
    setup_directories()
    engine = initialize_database(DB_PATH)
    logger.info("Module setup complete. Database and directories are ready.")
except Exception as e:
    logger.critical(f"Module setup failed: {e}")
    raise
