import yaml
import os


# Configuration Constants
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT: str = os.path.dirname(os.path.dirname(BASE_DIR))
DATA_DIR: str = os.path.join(PROJECT_ROOT, 'data')
IMAGES_DIR: str = os.path.join(PROJECT_ROOT, 'img')
GOOGLE_ICON_PATH: str = os.path.join(IMAGES_DIR, 'google_logo.svg')
TEMPLATES_DIR: str = os.path.join(PROJECT_ROOT, 'templates')

def get_api_key():
    # Load the YAML file
    with open(os.path.join('credentials', 'api.yml'), 'r') as f:
        config = yaml.safe_load(f)
    
    # Return the SERP_API_KEY value
    return config.get('SERP_API_KEY')