import yaml
import os

def get_api_key():
    # Load the YAML file
    with open(os.path.join('credentials', 'api.yml'), 'r') as f:
        config = yaml.safe_load(f)
    
    # Return the SERP_API_KEY value
    return config.get('SERP_API_KEY')