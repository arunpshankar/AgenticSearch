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
from src.tools.registry import get_public_ip_with_location
from src.tools.registry import get_random_dog_breed_image
from src.tools.registry import get_google_shopping_search
from src.tools.registry import get_google_search_results
from src.tools.registry import get_multimodal_reasoning
from src.tools.registry import get_walmart_basic_search
from src.tools.registry import get_youtube_basic_search
from src.tools.registry import get_multiple_dog_images
from src.tools.registry import get_random_joke_by_type
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
from src.tools.registry import get_exchange_rates
from src.llm.gemini_text import generate_content
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
from src.config.setup import MODEL
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
    ZIP_INFO = auto()
    PUBLIC_IP = auto()
    CURRENT_LOCATION = auto()
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
    """
    Represents a tool with a name and functionality.

    Attributes:
        name (Name): The name of the tool, represented as an enum member.
        func (Callable): The function to execute the tool's operation.
    """
    def __init__(self, name: Name, func: Callable):
        self.name = name
        self.func = func

    def use(self, query: Union[str, Dict[str, str], None] = None) -> Observation:
        """
        Executes the tool's function with the provided query.

        Args:
            query (Union[str, Dict[str, str], None]): The input query for the tool.
                Can be:
                - A string
                - A dictionary containing required keys
                - None (if the tool does not require an input)

        Returns:
            Observation: The result of the tool execution or an error message.
        """
        try:
            logger.info(f"Using tool: {self.name} with query: {query}")

            # Validate and process input
            if isinstance(query, dict):
                # Ensure the required arguments are present in the dictionary
                required_args = self.func.__code__.co_varnames[:self.func.__code__.co_argcount]
                missing_args = [arg for arg in required_args if arg not in query]
                if missing_args:
                    raise ValueError(f"Missing required arguments for tool {self.name}: {missing_args}")

                # Call the function with unpacked arguments
                result = self.func(**query)
            elif isinstance(query, str):
                # Pass string input directly
                result = self.func(query)
            elif query is None:
                # Call the function with no arguments if allowed
                result = self.func()
            else:
                raise ValueError(f"Invalid input type for tool {self.name}: {type(query)}")

            logger.info(f"Tool {self.name} executed successfully with result: {result}")
            return result
        except Exception as e:
            error_msg = f"Error executing tool {self.name}: {e}"
            logger.error(error_msg)
            return str(e)


class Message(BaseModel):
    """
    Represents a message in the system.

    Attributes:
        role (str): The role of the sender (e.g., "user", "system").
        content (str): The content of the message, which can be a string or serialized JSON.
    """
    role: str
    content: str

    @field_validator('content', mode='before')
    @classmethod
    def validate_content(cls, v):
        """
        Validates and serializes content into a string.

        Args:
            v (Union[str, Dict]): The input content.

        Returns:
            str: Serialized string content.
        """
        if isinstance(v, dict):
            return json.dumps(v)
        return str(v)

class MultimodalContent(BaseModel):
    """
    Represents multimodal content with text and image.

    Attributes:
        text (str): The textual content.
        image_path (str): The path to the associated image.
    """
    text: str
    image_path: str

    def to_dict(self) -> Dict[str, str]:
        """
        Converts the multimodal content to a dictionary.

        Returns:
            Dict[str, str]: A dictionary with text and image_path.
        """
        return {"text": self.text, "image_path": self.image_path}

class ActionState(BaseModel):
    """
    Represents the state of an action performed by a tool.

    Attributes:
        tool_name (str): The name of the tool used.
        input (str): The input provided to the tool.
        result (Optional[Any]): The result of the action, if available.
        status (str): The current status of the action (e.g., "pending", "completed", "failed").
    """
    tool_name: str
    input: str
    result: Optional[Any] = None
    status: str = "pending"


def create_message(role: str, content: Union[str, Dict, Any]) -> Message:
    """
    Creates a new Message object with the specified role and content.

    Args:
        role (str): The role associated with the message (e.g., 'user', 'assistant').
        content (Union[str, Dict, Any]): The content of the message. 
            Can be a string, dictionary, or any other data type compatible with the Message object.

    Returns:
        Message: A Message object initialized with the provided role and content.

    Raises:
        ValueError: If the Message object creation fails due to validation errors,
                    a ValueError is raised with details about the failure.
    """
    try:
        return Message(role=role, content=content)
    except ValidationError as e:
        raise ValueError(f"Message creation failed: {str(e)}")

class Agent:
    """
    Represents an intelligent agent capable of interacting with tools, maintaining action history,
    and executing tasks iteratively based on user input and model responses.

    Attributes:
        model (str): The name of the language model used by the agent.
        max_iterations (int): The maximum number of iterations allowed for processing a query.
        tools (Dict[Name, Tool]): A registry of tools available to the agent.
        messages (List[Message]): A log of messages exchanged between the user, system, and agent.
        query (str): The current query being processed.
        image_path (Optional[str]): Path to an image for multimodal queries.
        current_iteration (int): The current iteration count of the agent.
        template (str): The prompt template loaded for generating responses.
        client: The initialized client for interacting with the language model.
        action_history (List[ActionState]): A history of actions executed by the agent.
        last_action_result (Optional[Any]): The result of the last action executed by the agent.
    """

    def __init__(self, model: str, max_iterations: int) -> None:
        """
        Initialize the agent with a specified model and maximum iterations.

        Args:
            model (str): The model name to use for generating responses.
            max_iterations (int): Maximum iterations allowed for query processing.

        Raises:
            ValueError: If `model` is not a string or `max_iterations` is not a positive integer.
        """
        self.model = model
        self.tools: Dict[Name, Tool] = {}
        self.messages: List[Message] = []
        self.query = ""
        self.image_path = None
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.template = self.load_template()
        self.client = initialize_genai_client()
        self.action_history: List[ActionState] = []
        self.last_action_result: Optional[Any] = None

        if not isinstance(model, str):
            raise ValueError("Model must be a string")
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            raise ValueError("max_iterations must be a positive integer")

    def get_last_action_result(self) -> Optional[Any]:
        """
        Get the result of the last executed action.
        """
        if self.action_history:
            return self.action_history[-1].result
        return None

    def add_action_state(self, tool_name: str, input_query: str) -> None:
        """
        Add a new action state to history.

        Args:
            tool_name (str): The name of the tool used.
            input_query (str): The input query for the action.
        """
        self.action_history.append(ActionState(tool_name=tool_name, input=input_query))

    def update_last_action_state(self, result: Any, status: str) -> None:
        """
        Update the state of the last action.

        Args:
            result (Any): The result of the action.
            status (str): The status of the action (e.g., "completed" or "failed").
        """
        if self.action_history:
            last_action = self.action_history[-1]
            last_action.result = result
            last_action.status = status
            self.last_action_result = result

    def load_template(self) -> str:
        """
        Load the prompt template for generating responses."""
        return read_file(PROMPT_TEMPLATE_PATH)

    def register_tool(self, name: Name, func: Callable[[str], str]) -> None:
        """
        Register a tool for the agent.

        Args:
            name (Name): The name of the tool.
            func (Callable[[str], str]): The function to execute for the tool.
        """
        self.tools[name] = Tool(name, func)

    def trace(self, role: str, content: str) -> None:
        """
        Log a message in the message history.

        Args:
            role (str): The role of the message sender (e.g., "user" or "assistant").
            content (str): The content of the message.
        """
        if role != "system":
            self.messages.append(Message(role=role, content=content))

    def get_history(self) -> str:
        """
        Retrieve the conversation history including action results."""
        history = []
        for msg in self.messages:
            history.append(f"{msg.role}: {msg.content}")
        if self.last_action_result:
            history.append(f"Last action result: {json.dumps(self.last_action_result, indent=2)}")
        return "\n".join(history)

    def ask_gemini(self, prompt: str) -> dict:
        """
        Generate a response using the language model.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            dict: The response from the model, parsed as JSON.
        """
        try:
            if self.image_path:
                multimodal_input = {
                    "text": prompt,
                    "image_path": self.image_path
                }
                response = self.tools[Name.GEMINI_MULTIMODAL].use(multimodal_input)
            else:
                response = generate_content(self.client, self.model, prompt)
                response = str(response.text) if response else {"error": "No response from Gemini"}
            
            # Log raw response for debugging
            cleaned_response = response.strip().strip('`').strip()
            logger.info(f"Raw response before JSON parsing: {cleaned_response}")
            
            # Handle potential prefixes
            if cleaned_response.startswith('json'):
                cleaned_response = cleaned_response[4:].strip()
            
            # Validate and parse JSON
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError as jde:
                logger.error(f"JSON decode error: {jde} | Response: {cleaned_response}")
                return {"error": f"Invalid JSON response: {str(jde)}"}
        except Exception as e:
            logger.error(f"Error in ask_gemini: {e}")
            return {"error": str(e)}


    def think(self):
        """
        Generate the agent's next step based on the current query and context."""
        self.current_iteration += 1
        if self.current_iteration > self.max_iterations:
            self.trace("assistant",
                       "I couldn't find a satisfactory answer within the allowed iterations.")
            return None

        last_result = self.get_last_action_result()
        prompt = self.template.format(
            query=self.query,
            image_context=self.image_path,
            history=self.get_history(),
            tools=', '.join([str(t.name) for t in self.tools.values()]),
            last_result=json.dumps(last_result) if last_result else "None"
        )

        response = self.ask_gemini(prompt)
        if "error" in response:
            self.trace("assistant", f"Error in thinking: {response['error']}")
            return None

        self.trace("assistant", f"Thought: {response}")
        return response

    def decide_and_act(self, response: dict):
        """
        Interpret the model's response and execute the appropriate action.

        Args:
            response (dict): The response from the model, parsed as JSON.

        Returns:
            Optional[Any]: The final answer, if available.
        """
        try:
            if "action" in response:
                action = response["action"]
                name_str = action["name"].upper()

                if name_str == "NONE":
                    return None

                tool_name = Name[name_str]
                self.trace("assistant", f"Action: Using {tool_name} tool")

                if tool_name == Name.GEMINI_MULTIMODAL:
                    action_input = action.get("input", {})
                    if isinstance(action_input, str):
                        action_input = {"text": action_input}

                    query_input = {
                        "text": action_input.get("text", self.query),
                        "image_path": action_input.get("image_path", self.image_path)
                    }
                else:
                    query_input = action.get("input", self.query)

                self.add_action_state(name_str, str(query_input))

                result = self.tools[tool_name].use(query_input)

                if isinstance(result, Exception):
                    self.update_last_action_state(str(result), "failed")
                    observation = f"Error using {tool_name}: {result}"
                else:
                    self.update_last_action_state(result, "completed")
                    observation = f"Observation from {tool_name}: {result}"

                self.trace("system", observation)
                return None

            elif "answer" in response:
                final = response["answer"]
                self.trace("assistant", f"Final Answer: {final}")
                return final

            else:
                raise ValueError("Unrecognized JSON structure")

        except Exception as e:
            logger.error(f"Error in decide_and_act: {e}")
            self.trace("assistant", f"I encountered an error: {str(e)}. Let me try again.")
            return None

    def run_iter(self, query: Dict[str, Any]):
        """
        Run a single iteration of the agent's execution loop.

        Args:
            query (Dict[str, Any]): A dictionary containing the query text and optional image path.

        Yields:
            Dict[str, Any]: The state of the agent after each iteration.
        """
        logger.info(f'Raw Query: {query}')

        if isinstance(query, dict):
            self.query = query.get('text', '')
            self.image_path = query.get('image_path')
        else:
            self.query = str(query)
            self.image_path = None

        if self.image_path:
            query_content = {
                "text": self.query,
                "image_path": self.image_path
            }
        else:
            query_content = self.query

        self.trace("user", query_content)
        final_answer = None

        while final_answer is None and self.current_iteration < self.max_iterations:
            response = self.think()
            if response is None:
                yield {
                    "iteration": self.current_iteration,
                    "messages": [],
                    "done": True,
                }
                break

            iteration_messages = []
            start_index = len(self.messages) - 1

            if self.image_path and "action" in response:
                action = response["action"]
                if action["name"] != "GEMINI_MULTIMODAL":
                    # action["name"] = "GEMINI_MULTIMODAL"
                    action["input"] = {
                        "text": action.get("input", self.query),
                        "image_path": self.image_path
                    }
                    response["action"] = action

            final_answer = self.decide_and_act(response)
            end_index = len(self.messages)

            iteration_messages = self.messages[start_index:end_index]

            yield {
                "iteration": self.current_iteration,
                "messages": iteration_messages,
                "done": (final_answer is not None)
            }

        yield {
            "iteration": self.current_iteration,
            "messages": [],
            "done": True,
        }


def build_agent(max_iterations: int) -> Agent:
    """
    Helper function to instantiate an Agent, register all tools, and return it.

    Args:
        max_iterations (int): The maximum number of iterations the agent can perform.

    Returns:
        Agent: An instance of the Agent class with registered tools.
    """
    agent = Agent(model=MODEL, max_iterations=max_iterations)

    # Register tools for the agent
    agent.register_tool(Name.WIKI_SEARCH, get_wiki_search_results)
    agent.register_tool(Name.GOOGLE_SEARCH, get_google_search_results)
    agent.register_tool(Name.CAT_FACT, get_cat_fact)
    agent.register_tool(Name.WALMART_SEARCH, get_walmart_basic_search)
    agent.register_tool(Name.MULTIPLE_CAT_FACTS, get_multiple_cat_facts)
    agent.register_tool(Name.CAT_BREEDS, get_cat_breeds)
    agent.register_tool(Name.DOG_IMAGE, get_random_dog_image)
    agent.register_tool(Name.MULTIPLE_DOG_IMAGES, get_multiple_dog_images)
    agent.register_tool(Name.DOG_BREED_IMAGE, get_random_dog_breed_image)
    agent.register_tool(Name.RANDOM_JOKE, get_random_joke)
    agent.register_tool(Name.TEN_RANDOM_JOKES, get_ten_random_jokes)
    agent.register_tool(Name.RANDOM_JOKE_BY_TYPE, get_random_joke_by_type)
    agent.register_tool(Name.ZIP_INFO, get_zip_info)
    agent.register_tool(Name.PUBLIC_IP, get_public_ip)
    agent.register_tool(Name.CURRENT_LOCATION, get_public_ip_with_location)
    agent.register_tool(Name.ISS_LOCATION, get_iss_location)
    agent.register_tool(Name.LYRICS, get_lyrics)
    agent.register_tool(Name.RANDOM_FOX_IMAGE, get_random_fox_image)
    agent.register_tool(Name.TRIVIA_QUESTIONS, get_trivia_questions)
    agent.register_tool(Name.EXCHANGE_RATES, get_exchange_rates)
    agent.register_tool(Name.GOOGLE_IMAGE_SEARCH, get_google_image_search_results)
    agent.register_tool(Name.GOOGLE_NEWS_SEARCH, get_google_news_search)
    agent.register_tool(Name.GOOGLE_MAPS_SEARCH, get_google_maps_search)
    agent.register_tool(Name.GOOGLE_MAPS_PLACE, get_google_maps_place)
    agent.register_tool(Name.GOOGLE_JOBS_SEARCH, get_google_jobs_search)
    agent.register_tool(Name.GOOGLE_SHOPPING_SEARCH, get_google_shopping_search)
    agent.register_tool(Name.GOOGLE_TRENDS_INTEREST, get_google_trends_interest_over_time)
    agent.register_tool(Name.GOOGLE_TRENDS_BREAKDOWN, get_google_trends_compared_breakdown)
    agent.register_tool(Name.GOOGLE_TRENDS_REGION, get_google_trends_interest_by_region)
    agent.register_tool(Name.YOUTUBE_SEARCH, get_youtube_basic_search)
    agent.register_tool(Name.GOOGLE_PLAY_SEARCH, get_google_play_query_search)
    agent.register_tool(Name.GOOGLE_LOCAL_SEARCH, get_google_local_basic_search)
    agent.register_tool(Name.GOOGLE_VIDEOS_SEARCH, get_google_videos_basic_search)
    agent.register_tool(Name.GOOGLE_EVENTS_SEARCH, get_google_events_basic_search)
    agent.register_tool(Name.GOOGLE_FINANCE_SEARCH, get_google_finance_basic_search)
    agent.register_tool(Name.GOOGLE_FINANCE_CURRENCY_EXCHANGE, get_google_finance_currency_exchange)
    agent.register_tool(Name.GOOGLE_LOCATION_SPECIFIC_SEARCH, get_google_location_specific_search)
    agent.register_tool(Name.GEMINI_MULTIMODAL, get_multimodal_reasoning)

    return agent

def run_react_agent(query: str, max_iterations: int):
    """
    Executes the ReAct agent with the given query and maximum iterations.

    Args:
        query (str): The input query string for the agent to process.
        max_iterations (int): The maximum number of iterations the agent is allowed.

    Returns:
        Generator: A generator yielding data for each iteration, including messages and completion status.
    """
    agent = build_agent(max_iterations=max_iterations)
    return agent.run_iter(query)


if __name__ == "__main__":
    complex_query = {
        "text": "Tell me about the history of the Eiffel Tower and suggest some nearby attractions to visit.",
    }
    max_iterations = 10

    for iteration_data in run_react_agent(complex_query, max_iterations):
        logger.info(f"Iteration {iteration_data['iteration']}:")
        for message in iteration_data['messages']:
            logger.info(f"{message.role}: {message.content}")
        if iteration_data["done"]:
            logger.info("Task completed.")
            break
