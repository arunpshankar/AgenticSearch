from src.tools.registry import get_google_trends_interest_over_time
from src.tools.registry import get_google_trends_compared_breakdown
from src.tools.registry import get_google_trends_interest_by_region
from src.tools.registry import get_google_finance_currency_exchange
from src.tools.registry import get_google_location_specific_search
from src.tools.registry import get_google_image_search_results
from src.tools.registry import get_google_finance_basic_search
from src.tools.registry import get_google_events_basic_search
from src.tools.registry import get_google_videos_basic_search
from src.tools.registry import get_google_local_basic_search
from src.tools.registry import get_google_play_query_search
from src.tools.registry import get_random_dog_breed_image
from src.tools.registry import get_google_shopping_search
from src.tools.registry import get_predicted_age_by_name
from src.tools.registry import get_google_search_results
from src.tools.registry import get_multimodal_reasoning
from src.tools.registry import get_walmart_basic_search
from src.tools.registry import get_youtube_basic_search
from src.tools.registry import get_multiple_dog_images
from src.tools.registry import get_random_joke_by_type
from src.tools.registry import get_nationality_by_name
from src.tools.registry import get_wiki_search_results
from src.tools.registry import get_multiple_cat_facts
from src.tools.registry import get_google_news_search
from src.tools.registry import get_google_maps_search
from src.tools.registry import get_google_jobs_search
from src.config.setup import initialize_genai_client
from src.tools.registry import get_google_maps_place
from src.tools.registry import get_random_dog_image
from src.tools.registry import get_ten_random_jokes
from src.tools.registry import get_random_fox_image
from src.tools.registry import get_trivia_questions
from src.tools.registry import get_gender_by_name
from src.tools.registry import get_exchange_rates
from src.llm.gemini_text import generate_content
from src.tools.registry import get_artwork_data
from src.tools.registry import get_iss_location
from src.tools.registry import get_random_joke
from src.tools.registry import get_cat_breeds
from src.tools.registry import get_public_ip
from src.tools.registry import get_cat_fact
from src.tools.registry import get_zip_info
from src.tools.registry import get_lyrics
from src.config.logging import logger
from pydantic import ValidationError
from pydantic import field_validator
from src.utils.io import read_file
from pydantic import BaseModel
from typing import Callable
from typing import Optional
from typing import Union
from typing import List 
from typing import Dict 
from typing import Any 
from enum import Enum
from enum import auto 
import json

Observation = Union[str, Exception]
PROMPT_TEMPLATE_PATH = "./templates/react.txt"

class Name(Enum):
    WIKI_SEARCH = auto()
    GOOGLE_SEARCH = auto()
    MULTIPLE_CAT_FACTS = auto()
    CAT_FACT = auto()
    CAT_BREEDS = auto()
    DOG_IMAGE = auto()
    MULTIPLE_DOG_IMAGES = auto()
    DOG_BREED_IMAGE = auto()
    RANDOM_JOKE = auto()
    TEN_RANDOM_JOKES = auto()
    RANDOM_JOKE_BY_TYPE = auto()
    PREDICT_AGE = auto()
    PREDICT_GENDER = auto()
    PREDICT_NATIONALITY = auto()
    ZIP_INFO = auto()
    PUBLIC_IP = auto()
    ARTWORK_DATA = auto()
    ISS_LOCATION = auto()
    LYRICS = auto()
    RANDOM_FOX_IMAGE = auto()
    TRIVIA_QUESTIONS = auto()
    EXCHANGE_RATES = auto()
    GOOGLE_IMAGE_SEARCH = auto()
    GOOGLE_NEWS_SEARCH = auto()
    GOOGLE_MAPS_SEARCH = auto()
    GOOGLE_MAPS_PLACE = auto()
    GOOGLE_JOBS_SEARCH = auto()
    GOOGLE_SHOPPING_SEARCH = auto()
    GOOGLE_TRENDS_INTEREST = auto()
    GOOGLE_TRENDS_BREAKDOWN = auto()
    GOOGLE_TRENDS_REGION = auto()
    GOOGLE_LENS_SEARCH = auto()
    GOOGLE_PLAY_SEARCH = auto()
    GOOGLE_LOCAL_SEARCH = auto()
    GOOGLE_EVENTS_SEARCH = auto()
    GOOGLE_VIDEOS_SEARCH = auto()
    GOOGLE_REVERSE_IMAGE_SEARCH = auto()
    GOOGLE_FINANCE_SEARCH = auto()
    GOOGLE_FINANCE_CURRENCY_EXCHANGE = auto()
    GOOGLE_LOCATION_SPECIFIC_SEARCH = auto()
    WALMART_SEARCH = auto()
    YOUTUBE_SEARCH = auto()
    GEMINI_MULTIMODAL = auto()
    NONE = "none"

class Tool:
    def __init__(self, name: Name, func: Callable[[Union[str, Dict[str, str]]], str]):
        self.name = name
        self.func = func

    def use(self, query: Union[str, Dict[str, str]]) -> Observation:
        try:
            return self.func(query)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            return str(e)
        
class Message(BaseModel):
    role: str
    content: str

    # Use mode="before" to intercept the raw input before pydantic enforces string type
    @field_validator('content', mode='before')
    @classmethod
    def validate_content(cls, v):
        if isinstance(v, dict):
            return json.dumps(v)
        return str(v)
class MultimodalContent(BaseModel):
    text: str
    image_path: str

    def to_dict(self) -> Dict[str, str]:
        return {"text": self.text, "image_path": self.image_path}

def create_message(role: str, content: Union[str, Dict, Any]) -> Message:
    try:
        return Message(role=role, content=content)
    except ValidationError as e:
        raise ValueError(f"Message creation failed: {str(e)}")

class ActionState(BaseModel):
    tool_name: str
    input: str
    result: Optional[Any] = None
    status: str = "pending"  # pending, completed, failed