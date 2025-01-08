from typing import Dict
from typing import Any 
import requests
from src.config.logging import logger 

def get_public_ip_with_location() -> Dict[str, Any]:
    """
    Retrieves the public IP address and its approximate location.

    :return: A dictionary containing the public IP address and location details.
    :raises requests.HTTPError: If the request fails.
    """
    ip_base_url = "https://api.ipify.org"
    ip_params = {"format": "json"}
    geo_base_url = "http://ip-api.com/json"  # or "https://ipinfo.io/{ip}/json"
    
    try:
        # Step 1: Get the public IP address
        ip_response = requests.get(ip_base_url, params=ip_params)
        ip_response.raise_for_status()
        ip_info = ip_response.json()
        public_ip = ip_info.get("ip")
        logger.info(f"Retrieved public IP: {public_ip}")
        
        # Step 2: Get the location of the IP address
        geo_response = requests.get(f"{geo_base_url}/{public_ip}")
        geo_response.raise_for_status()
        geo_info = geo_response.json()
        logger.info(f"Retrieved geolocation info: {geo_info}")
        
        return {"ip": public_ip, "location": geo_info}
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve public IP or geolocation: {e}")
        raise

if __name__ == '__main__':
    get_public_ip_with_location('')