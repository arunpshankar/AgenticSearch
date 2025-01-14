from src.llm.gemini_text_image import generate_multimodal_content
from src.config.setup import get_serp_api_key
from src.config.logging import logger
from typing import Optional
from typing import Union
from typing import Dict 
from typing import List 
from typing import Any 
import wikipediaapi
import requests
import json
import os 


def get_wiki_search_results(query: str) -> Optional[str]:
    """
    Fetch Wikipedia information for a given search query using Wikipedia-API and return as JSON.

    Args:
        query (str): The search query string.

    Returns:
        Optional[str]: A JSON string containing the query, title, and summary, or None if no result is found.
    """
    # Initialize Wikipedia API with a user agent
    wiki = wikipediaapi.Wikipedia(user_agent='ReAct Agents (shankar.arunp@gmail.com)',
                                  language='en')

    try:
        logger.info(f"Searching Wikipedia for: {query}")
        page = wiki.page(query)

        if page.exists():
            # Create a dictionary with query, title, and summary
            result = {
                "query": query,
                "title": page.title,
                "summary": page.summary
            }
            logger.info(f"Successfully retrieved summary for: {query}")
            return json.dumps(result, ensure_ascii=False, indent=2)
        else:
            logger.info(f"No results found for query: {query}")
            return None

    except Exception as e:
        logger.exception(f"An error occurred while processing the Wikipedia query: {e}")
        return None


def get_cat_fact(max_length: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve a random cat fact. Optionally, specify a maximum length for the fact.

    :param max_length: Maximum length of the cat fact (optional).
    :return: A dictionary containing the cat fact.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://catfact.ninja/fact"
    params = {"max_length": max_length} if max_length else {}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        fact = response.json()
        logger.info(f"Retrieved cat fact: {fact}")
        return fact
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve cat fact: {e}")
        raise


def get_multiple_cat_facts(limit: int) -> Dict[str, Any]:
    """
    Retrieve multiple cat facts.

    :param limit: Number of cat facts to retrieve.
    :return: A dictionary containing the cat facts.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://catfact.ninja/facts"
    params = {"limit": limit}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        facts = response.json()
        logger.info(f"Retrieved {limit} cat facts: {facts}")
        return facts
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve multiple cat facts: {e}")
        raise


def get_cat_breeds(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve a list of cat breeds.

    :param limit: Number of cat breeds to retrieve (optional).
    :return: A dictionary containing the list of cat breeds.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://catfact.ninja/breeds"
    params = {"limit": limit} if limit else {}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        breeds = response.json()
        logger.info(f"Retrieved cat breeds: {breeds}")
        return breeds
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve cat breeds: {e}")
        raise


def get_random_dog_image() -> Dict[str, Any]:
    """
    Retrieve a random dog image.

    :return: A dictionary containing the dog image URL.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://dog.ceo/api/breeds/image/random"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        image = response.json()
        logger.info(f"Retrieved dog image: {image}")
        return image
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve dog image: {e}")
        raise


def get_multiple_dog_images(number: int) -> Dict[str, Any]:
    """
    Retrieve multiple random dog images.

    :param number: Number of dog images to retrieve.
    :return: A dictionary containing the dog image URLs.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://dog.ceo/api/breeds/image/random/{number}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        images = response.json()
        logger.info(f"Retrieved {number} random dog images: {images}")
        return images
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random dog images: {e}")
        raise


def get_random_dog_breed_image(breed: str) -> Dict[str, Any]:
    """
    Retrieve a random image of a specific dog breed.

    :param breed: The breed of the dog.
    :return: A dictionary containing the dog image URL.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://dog.ceo/api/breed/{breed}/images/random"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        image = response.json()
        logger.info(f"Retrieved random dog image for breed '{breed}': {image}")
        return image
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random dog image for breed '{breed}': {e}")
        raise


def get_random_joke() -> Dict[str, Any]:
    """
    Retrieve a random joke.

    :return: A dictionary containing the joke.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        joke = response.json()
        logger.info(f"Retrieved random joke: {joke}")
        return joke
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random joke: {e}")
        raise


def get_ten_random_jokes() -> List[Dict[str, Any]]:
    """
    Retrieve ten random jokes.

    :return: A list of dictionaries containing jokes.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://official-joke-api.appspot.com/random_ten"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        jokes = response.json()
        logger.info(f"Retrieved ten random jokes: {jokes}")
        return jokes
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve ten random jokes: {e}")
        raise


def get_random_joke_by_type(joke_type: str) -> Dict[str, Any]:
    """
    Retrieve a random joke of a specific type.

    :param joke_type: The type of joke to retrieve (e.g., 'programming').
    :return: A dictionary containing the joke.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://official-joke-api.appspot.com/jokes/{joke_type}/random"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        joke = response.json()
        logger.info(f"Retrieved random joke of type '{joke_type}': {joke}")
        return joke
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random joke of type '{joke_type}': {e}")
        raise


def get_zip_info(zip_code: str) -> Dict[str, Any]:
    """
    Provides location data for U.S. ZIP codes.

    :param zip_code: The ZIP code to retrieve information for.
    :return: A dictionary containing location data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://api.zippopotam.us/us/{zip_code}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        zip_info = response.json()
        logger.info(f"Retrieved ZIP info for '{zip_code}': {zip_info}")
        return zip_info
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve ZIP info for '{zip_code}': {e}")
        raise


def get_public_ip() -> Dict[str, Any]:
    """
    Returns the public IP address of the requester.

    :return: A dictionary containing the public IP address.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://api.ipify.org"
    params = {"format": "json"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        ip_info = response.json()
        logger.info(f"Retrieved public IP: {ip_info}")
        return ip_info
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve public IP: {e}")
        raise


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
        response = requests.get(ip_base_url, params=ip_params)
        response.raise_for_status()
        ip_info = response.json()
        public_ip = ip_info.get("ip")
        logger.info(f"Retrieved public IP: {public_ip}")

        # Step 2: Get the location of the IP address
        location_response = requests.get(f"{geo_base_url}/{public_ip}")
        location_response.raise_for_status()
        location_info = location_response.json()
        logger.info(f"Retrieved geolocation info: {location_info}")

        return {"ip": public_ip, "location": location_info}

    except requests.RequestException as e:
        logger.error(f"Failed to retrieve public IP or geolocation: {e}")
        raise


def get_iss_location() -> Dict[str, Any]:
    """
    Get the current location of the International Space Station.

    :return: A dictionary containing the ISS position.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        iss_location = response.json()
        logger.info(f"Retrieved ISS location: {iss_location}")
        return iss_location
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve ISS location: {e}")
        raise


def get_lyrics(artist: str, title: str) -> Dict[str, Any]:
    """
    Fetch song lyrics by artist and title.

    :param artist: The artist's name.
    :param title: The song title.
    :return: A dictionary containing the song lyrics.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        lyrics = response.json()
        logger.info(f"Retrieved lyrics for '{artist} - {title}': {lyrics}")
        return lyrics
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve lyrics for '{artist} - {title}': {e}")
        raise


def get_random_fox_image() -> Dict[str, Any]:
    """
    Provides a random image of a fox.

    :return: A dictionary containing the image URL and link.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://randomfox.ca/floof/"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        fox_image = response.json()
        logger.info(f"Retrieved random fox image: {fox_image}")
        return fox_image
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve random fox image: {e}")
        raise


def get_trivia_questions(amount: Optional[int] = 1, category: Optional[int] = None, difficulty: Optional[str] = None, question_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Offers random trivia questions.

    :param amount: Number of questions to retrieve.
    :param category: Category of trivia questions.
    :param difficulty: Difficulty level (e.g., 'easy').
    :param question_type: Type of question (e.g., 'multiple').
    :return: A dictionary containing trivia questions.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://opentdb.com/api.php"
    params = {"amount": amount}
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty
    if question_type:
        params["type"] = question_type
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        trivia_data = response.json()
        logger.info(f"Retrieved trivia questions: {trivia_data}")
        return trivia_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve trivia questions: {e}")
        raise


def get_exchange_rates(base: Optional[str] = "USD") -> Dict[str, Any]:
    """
    Provides current and historical exchange rates.

    :param base: The base currency code (default: 'USD').
    :return: A dictionary containing exchange rates.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        exchange_data = response.json()
        logger.info(f"Retrieved exchange rates for base '{base}': {exchange_data}")
        return exchange_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve exchange rates for base '{base}': {e}")
        raise


def get_google_search_results(q: str, location: Optional[str] = None, google_domain: Optional[str] = None, gl: Optional[str] = None, hl: Optional[str] = None, safe: Optional[str] = None, num: Optional[int] = None, start: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve Google search results using SerpApi.

    :param q: Search query (required).
    :param location: Location for the search (optional).
    :param google_domain: Google domain to use (optional).
    :param gl: Country code for the search (optional).
    :param hl: Language for the search (optional).
    :param safe: Safe search setting (optional).
    :param num: Number of results to return (optional).
    :param start: Starting index for results (optional).
    :return: A dictionary containing the search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "api_key": get_serp_api_key()}
    if location:
        params["location"] = location
    if google_domain:
        params["google_domain"] = google_domain
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    if safe:
        params["safe"] = safe
    if num:
        params["num"] = num
    if start:
        params["start"] = start
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        logger.info(f"Retrieved Google search results for query '{q}': {search_results}")
        return search_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google search results for query '{q}': {e}")
        raise


def get_google_image_search_results(q: str, tbm: str = "isch", gl: Optional[str] = None, hl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve Google Images search results using SerpApi.

    :param q: Search query (required).
    :param tbm: Specifies image search (required, default is 'isch').
    :param gl: Country code for the search (optional).
    :param hl: Language for the search (optional).
    :return: A dictionary containing the image search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "tbm": tbm, "api_key": get_serp_api_key()}
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        image_results = response.json()
        logger.info(f"Retrieved Google Images search results for query '{q}': {image_results}")
        return image_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Images search results for query '{q}': {e}")
        raise


def get_google_location_specific_search(q: str, location: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve Google search results simulating queries from a given geographic location.

    :param q: Search query (required).
    :param location: Geographic location (optional).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :return: A dictionary containing location-specific search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "api_key": get_serp_api_key()}
    if location:
        params["location"] = location
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        location_results = response.json()
        logger.info(f"Retrieved location-specific search results for query '{q}': {location_results}")
        return location_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve location-specific search results for query '{q}': {e}")
        raise


def get_google_news_search(q: str, tbm: str = "nws", hl: Optional[str] = None, gl: Optional[str] = None, num: Optional[int] = None, start: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve Google News search results using SerpApi.

    :param q: Search query (required).
    :param tbm: Specifies news search (required, default is 'nws').
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param num: Number of results to return (optional).
    :param start: Starting index for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing the news search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"q": q, "tbm": tbm, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if num:
        params["num"] = num
    if start:
        params["start"] = start
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        news_results = response.json()
        logger.info(f"Retrieved Google News search results for query '{q}': {news_results}")
        return news_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google News search results for query '{q}': {e}")
        raise


def get_google_maps_search(q: Optional[str] = None, ll: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, start: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve Google Maps search results from SerpApi.

    :param q: Search query (optional).
    :param ll: Latitude and longitude coordinates (optional).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param start: Starting index for results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing Google Maps search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_maps", "api_key": get_serp_api_key()}
    if q:
        params["q"] = q
    if ll:
        params["ll"] = ll
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if start:
        params["start"] = start
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        maps_results = response.json()
        logger.info(f"Retrieved Google Maps search results for query '{q}': {maps_results}")
        return maps_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Maps search results for query '{q}': {e}")
        raise


def get_google_maps_place(place_id: str, hl: Optional[str] = None, gl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve details of a specific place on Google Maps using place_id.

    :param place_id: The place ID (required).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing place details.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_maps", "place_id": place_id, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        place_details = response.json()
        logger.info(f"Retrieved place details for place ID '{place_id}': {place_details}")
        return place_details
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve place details for place ID '{place_id}': {e}")
        raise


def get_google_jobs_search(q: str, location: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None, lrad: Optional[int] = None, ltype: Optional[str] = None, next_page_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve Google Jobs search results from SerpApi.

    :param q: Search query (required).
    :param location: Location for the job search (optional).
    :param hl: Language for the search (optional).
    :param gl: Country code for the search (optional).
    :param lrad: Search radius in miles (optional).
    :param ltype: Location type (e.g., 'city') (optional).
    :param next_page_token: Token for the next page of results (optional).
    :param api_key: SerpApi API key (required).
    :return: A dictionary containing job search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_jobs", "q": q, "api_key": get_serp_api_key()}
    if location:
        params["location"] = location
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if lrad:
        params["lrad"] = lrad
    if ltype:
        params["ltype"] = ltype
    if next_page_token:
        params["next_page_token"] = next_page_token
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        jobs_results = response.json()
        logger.info(f"Retrieved Google Jobs search results for query '{q}': {jobs_results}")
        return jobs_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Jobs search results for query '{q}': {e}")
        raise


def get_google_shopping_search(q: str, location: Optional[str] = None, google_domain: Optional[str] = None, gl: Optional[str] = None, hl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve Google Shopping search results from SerpApi.

    :param q: Search query (required).
    :param location: Location for the search (optional).
    :param google_domain: Google domain to use (optional).
    :param gl: Country code for the search (optional).
    :param hl: Language for the search (optional).
    :return: A dictionary containing shopping search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_shopping", "q": q, "api_key": get_serp_api_key()}
    if location:
        params["location"] = location
    if google_domain:
        params["google_domain"] = google_domain
    if gl:
        params["gl"] = gl
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        shopping_results = response.json()
        logger.info(f"Retrieved Google Shopping search results for query '{q}': {shopping_results}")
        return shopping_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Shopping search results for query '{q}': {e}")
        raise


def get_walmart_basic_search(query: str, page: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieve Walmart search results using a query from SerpApi.

    :param query: Search query (required).
    :param page: Page number for results (optional).
    :return: A dictionary containing Walmart search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "walmart", "query": query, "api_key": get_serp_api_key()}
    if page:
        params["page"] = page
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        search_results = response.json()
        logger.info(f"Retrieved Walmart search results for query '{query}': {search_results}")
        return search_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Walmart search results for query '{query}': {e}")
        raise


def get_google_local_basic_search(q: str, location: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve local business results by query using SerpApi's Google Local API.

    :param q: Search query (required).
    :param location: Location for the search (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :return: A dictionary containing local business results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_local", "q": q, "api_key": get_serp_api_key()}
    if location:
        params["location"] = location
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        local_results = response.json()
        logger.info(f"Retrieved Google Local search results for query '{q}': {local_results}")
        return local_results
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Local search results for query '{q}': {e}")
        raise


def get_google_finance_basic_search(q: str, hl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve Google Finance data for a given ticker or search query from SerpApi.

    :param q: Search query or ticker (required).
    :param hl: Language for the search (optional).
    :return: A dictionary containing Google Finance data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_finance", "q": q, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        finance_data = response.json()
        logger.info(f"Retrieved Google Finance data for query '{q}': {finance_data}")
        return finance_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Finance data for query '{q}': {e}")
        raise


def get_google_finance_currency_exchange(q: str, hl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve exchange rate data for a currency pair using SerpApi.

    :param q: Currency pair (e.g., 'USD/EUR') (required).
    :param hl: Language for the search (optional).
    :return: A dictionary containing currency exchange rate data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_finance", "q": q, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        exchange_data = response.json()
        logger.info(f"Retrieved currency exchange data for query '{q}': {exchange_data}")
        return exchange_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve currency exchange data for query '{q}': {e}")
        raise


def get_google_events_basic_search(q: str, hl: Optional[str] = None, gl: Optional[str] = None, location: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve events based on a query using SerpApi's Google Events API.

    :param q: Search query (e.g., 'Events in Austin, TX') (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :param location: Location for the events (optional).
    :return: A dictionary containing events data.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_events", "q": q, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    if location:
        params["location"] = location
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        events_data = response.json()
        logger.info(f"Retrieved events for query '{q}': {events_data}")
        return events_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve events for query '{q}': {e}")
        raise


def get_google_play_query_search(q: Optional[str] = None, hl: Optional[str] = None, gl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve app listings from the Google Play Store by search query using SerpApi.

    :param q: Search query (optional).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :return: A dictionary containing app listings.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_play", "api_key": get_serp_api_key()}
    if q:
        params["q"] = q
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        play_data = response.json()
        logger.info(f"Retrieved Google Play app listings for query '{q}': {play_data}")
        return play_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Play app listings for query '{q}': {e}")
        raise


def get_google_videos_basic_search(q: str, hl: Optional[str] = None, gl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve video search results from Google Videos by query using SerpApi.

    :param q: Search query (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :return: A dictionary containing video search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "google_videos", "q": q, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        video_data = response.json()
        logger.info(f"Retrieved Google Videos results for query '{q}': {video_data}")
        return video_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve Google Videos results for query '{q}': {e}")
        raise


def get_youtube_basic_search(q: str, hl: Optional[str] = None, gl: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve YouTube search results by providing a search query using SerpApi.

    :param q: Search query (required).
    :param hl: Language for the search (optional).
    :param gl: Geographic region for the search (optional).
    :return: A dictionary containing YouTube search results.
    :raises requests.HTTPError: If the request fails.
    """
    base_url = "https://serpapi.com/search"
    params = {"engine": "youtube", "search_query": q, "api_key": get_serp_api_key()}
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        youtube_data = response.json()
        logger.info(f"Retrieved YouTube results for query '{q}': {youtube_data}")
        return youtube_data
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve YouTube results for query '{q}': {e}")
        raise


def get_multimodal_reasoning(q: Union[str, Dict[str, str]]) -> str:
    """
    Perform multimodal reasoning on text and image inputs using Gemini model.
    
    Args:
        q (Union[str, Dict[str, str]]): Either:
            - A dictionary containing {"text": str, "image_path": str}
            - A JSON string containing {"text": str, "image_path": str}
    
    Returns:
        str: Generated reasoning/response from Gemini model
        
    Raises:
        ValueError: If inputs are invalid or image cannot be loaded
        Exception: For other errors during processing
    """
    try:
        # Parse input to extract text and image_path
        if isinstance(q, str):
            try:
                # Try parsing as JSON string
                input_dict = json.loads(q)
            except json.JSONDecodeError:
                # If not JSON, assume it's a text query
                raise ValueError("Invalid input format. Expected JSON string or dictionary")
        else:
            input_dict = q
            
        # Extract required fields
        if not isinstance(input_dict, dict):
            raise ValueError("Input must be a dictionary or JSON string")
            
        text = input_dict.get('text')
        image_path = input_dict.get('image_path')
        
        # Validate inputs
        if not text or not text.strip():
            raise ValueError("Query text cannot be empty")
        if not image_path or not os.path.exists(image_path):
            raise ValueError(f"Invalid image path: {image_path}")
            
        logger.info(f"Starting multimodal reasoning with query: {text}")
        logger.info(f"Using image from path: {image_path}")
        
        # Generate response using multimodal content function
        response = generate_multimodal_content(text, image_path)
        logger.info("Successfully generated multimodal response")
        
        return response
    except Exception as e:
        error_msg = f"Failed to perform multimodal reasoning: {str(e)}"
        logger.error(error_msg)
        raise


if __name__ == "__main__":
    tests_passed = 0
    tests_failed = 0

    def run_test(test_name: str, func, *args, **kwargs):
        """
        Run a test case and log the result.

        :param test_name: Name of the test.
        :param func: Function to test.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        global tests_passed, tests_failed
        try:
            result = func(*args, **kwargs)
            logger.info(f"Test '{test_name}' passed. Output: {result}")
            tests_passed += 1
        except Exception as e:
            logger.error(f"Test '{test_name}' failed. Error: {e}")
            tests_failed += 1

    # Running tests
    run_test("get_wiki_search_results", get_wiki_search_results, "Python (programming language)")
    run_test("get_cat_fact", get_cat_fact)
    run_test("get_cat_fact with max_length", get_cat_fact, max_length=50)
    run_test("get_multiple_cat_facts", get_multiple_cat_facts, limit=3)
    run_test("get_cat_breeds", get_cat_breeds, limit=2)
    run_test("get_random_dog_image", get_random_dog_image)
    run_test("get_multiple_dog_images", get_multiple_dog_images, number=3)
    run_test("get_random_dog_breed_image", get_random_dog_breed_image, breed="hound")
    run_test("get_random_joke", get_random_joke)
    run_test("get_ten_random_jokes", get_ten_random_jokes)
    run_test("get_random_joke_by_type", get_random_joke_by_type, joke_type="programming")
    run_test("get_random_fox_image", get_random_fox_image)
    run_test("get_trivia_questions", get_trivia_questions, amount=1)
    run_test("get_exchange_rates", get_exchange_rates, base="USD")
    run_test("get_zip_info", get_zip_info, zip_code="90210")
    run_test("get_public_ip", get_public_ip)
    run_test("get_public_ip_with_location", get_public_ip_with_location)
    run_test("get_iss_location", get_iss_location)
    run_test("get_lyrics", get_lyrics, artist="Adele", title="Hello")
    run_test("get_google_search_results", get_google_search_results, q="coffee", location="New York,NY,United States", hl="en", gl="us")
    run_test("get_google_image_search_results", get_google_image_search_results, q="cat memes", hl="en", gl="us")
    run_test("get_google_location_specific_search", get_google_location_specific_search, q="best pizza", location="Chicago,Illinois,United States", hl="en", gl="us")
    run_test("get_google_news_search", get_google_news_search, q="technology news", tbm="nws", hl="en", gl="us")
    run_test("get_google_maps_search", get_google_maps_search, q="Coffee", ll="@40.7455096,-74.0083012,14z")
    run_test("get_google_maps_place", get_google_maps_place, place_id="ChIJ9Sto4ahZwokRXpWiQYiOOOo")
    run_test("get_google_jobs_search", get_google_jobs_search, q="software engineer", location="New York,NY", hl="en", gl="us")
    run_test("get_google_shopping_search", get_google_shopping_search, q="coffee mug", gl="us", hl="en")
    run_test("get_walmart_basic_search", get_walmart_basic_search, query="coffee maker", page=1)
    run_test("get_google_local_basic_search", get_google_local_basic_search, q="coffee shops", location="New York,NY", hl="en", gl="us")
    run_test("get_google_finance_basic_search", get_google_finance_basic_search, q="NASDAQ:GOOGL", hl="en")
    run_test("get_google_finance_currency_exchange", get_google_finance_currency_exchange, q="USD/EUR", hl="en")
    run_test("get_google_events_basic_search", get_google_events_basic_search, q="Events in Austin TX", hl="en", gl="us", location="Austin,Texas,United States")
    run_test("get_google_play_query_search", get_google_play_query_search, q="weather apps", hl="en", gl="us")
    run_test("get_google_videos_basic_search", get_google_videos_basic_search, q="funny cats", hl="en", gl="us")
    run_test("get_youtube_basic_search", get_youtube_basic_search, q="star wars", hl="en", gl="us")
    run_test("get_multimodal_reasoning", get_multimodal_reasoning, q=json.dumps({"text": "What's in this image?", "image_path": "./tmp/uploads/sample.jpg"}))

    logger.info(f"Tests completed. Passed: {tests_passed}, Failed: {tests_failed}")