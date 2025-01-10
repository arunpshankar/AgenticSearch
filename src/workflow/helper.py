from src.config.setup import initialize_genai_client
from src.llm.gemini_text import generate_content
from src.config.setup import GOOGLE_ICON_PATH
from src.utils.template import TemplateLoader
from src.agents.react import run_react_agent
from src.config.logging import logger
from typing import Optional
from typing import Tuple
from typing import Dict
from typing import List 
from typing import Any 
import streamlit as st 
import datetime
import base64
import json 
import ast
import re
import os 

template_loader = TemplateLoader()


def extract_image_urls_from_observation(observation: Dict) -> List[str]:
    """
    Extracts image URLs from a SerpAPI image search observation result.
    
    This function handles various formats of the observation result and 
    traverses its structure to find and extract image URLs. It supports 
    different keys used for image results and URL fields within those results.

    Args:
        observation (Dict): The observation result from the image_search tool.
                                 Can be a nested dictionary or a string 
                                 representation of a dictionary.

    Returns:
        List[str]: A list of extracted image URLs.
    """
    image_urls = []
    
    try:
        # If the observation is a string, try to parse it into a dictionary
        if isinstance(observation, str):
            try:
                observation = ast.literal_eval(observation)
            except (ValueError, SyntaxError) as e:
                logger.error(f"Failed to parse observation string: {e}")
                return image_urls

        # Ensure the observation is now a dictionary
        if not isinstance(observation, dict):
            logger.error(f"Invalid observation type after parsing: {type(observation)}")
            return image_urls

        # Traverse nested dictionaries to find the actual image results
        if 'observation' in observation:
            observation = observation['observation']

        # Handle cases where the nested observation is also a string
        if isinstance(observation, str):
            try:
                observation = ast.literal_eval(observation)
            except (ValueError, SyntaxError) as e:
                logger.error(f"Failed to parse nested observation string: {e}")
                return image_urls

        # Look for image results under different possible keys
        if 'image_results' in observation:
            results = observation['image_results']
        elif 'images_results' in observation:
            results = observation['images_results']
        elif 'inline_images' in observation:
            results = observation['inline_images']
        else:
            logger.warning("No recognized image results field found.")
            logger.debug(f"Available keys: {observation.keys()}")
            return image_urls

        # Extract URLs from the located results
        for result in results:
            if isinstance(result, dict):
                # Try different possible URL fields within each result
                for field in ['original', 'link', 'image', 'thumbnail', 'original_image']:
                    if field in result and result[field]:
                        url = result[field]
                        if isinstance(url, str) and url.startswith('http'):
                            image_urls.append(url)
                            break

    except Exception as e:
        logger.error(f"Error extracting image URLs from observation: {e}")
        logger.exception(e)  # Log the full traceback

    return image_urls[:5] # retain only 1st 5 images 


def extract_and_clean_text(text: str) -> tuple[list[str], str]:
    """
    Extracts image URLs and cleans up the text for readability.
    """
    try:
        def extract_image_urls(text):
            # Define a regex pattern to extract valid URLs
            image_url_pattern = r'https?://[^\s\]\)]+'
            return re.findall(image_url_pattern, text)

        # Extract URLs using helper function
        urls = extract_image_urls(text)

        # Remove duplicates while maintaining order
        seen = set()
        urls = [url for url in urls if not (url in seen or seen.add(url))][:5]
        return urls, text

    except Exception as e:
        logger.error(f"Error in extract_and_clean_text: {e}")
        logger.exception(e)
        return [], text  # Return empty list for URLs and original text in case of error
    

def parse_thought_action(text: str) -> tuple[str, str]:
    """
    Parses 'thought' and 'action' from an LLM's JSON response inside triple backticks.
    Returns (thought, action_string).
    """
    try:
        # 1. Extract the JSON block between ```json ... ```
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if not match:
            # If there's no triple-backtick JSON block, fallback to some default
            return text, text
        
        json_content = match.group(1)
        
        # 2. Parse JSON
        data = json.loads(json_content)
        
        # 3. Extract fields
        thought = data.get('thought', '')
        action = data.get('action', {})
        
        # 4. Convert the action dictionary to a human-friendly string if needed
        if isinstance(action, dict):
            action_str = (
                f"Using {action.get('name', '')} tool\n"
                f"Reason: {action.get('reason', '')}\n"
                f"Input: {action.get('input', '')}"
            )
        else:
            action_str = str(action)
        
        return thought, action_str

    except Exception as e:
        logger.error(f"Error parsing thought and action from text: {e}")
        logger.exception(e)
        return text, text
    

def display_message(role: str, content: str, final_answer_container=None):
    """
    Displays a message with appropriate formatting and handles image extraction.
    """
    # 1. Convert content to string if needed
    content = _convert_content_to_string(content)

    # 2. Split the content into blocks based on markers
    blocks = _extract_blocks(content)

    # 3. Render each block
    _render_blocks(blocks, role, final_answer_container)


def _convert_content_to_string(content) -> str:
    """
    Safely convert the content to a string.
    """
    if not isinstance(content, str):
        try:
            content = str(content)
        except Exception as e:
            logger.error(f"Error converting content to string: {e}")
            content = "Error: Invalid message format"
    return content


def _extract_blocks(content: str):
    """
    Splits the content into blocks by recognized markers ('Thought:', 'Action:', 'Final Answer:', 'Error:').
    Each block is returned as a tuple (block_type, text).
    """
    markers = ["Thought:", "Action:", "Final Answer:", "Error:"]
    blocks = []
    
    pos = 0
    while pos < len(content):
        next_marker_pos = len(content)
        next_marker = None
        
        for m in markers:
            find_pos = content.find(m, pos)
            if find_pos != -1 and find_pos < next_marker_pos:
                next_marker_pos = find_pos
                next_marker = m
        
        if next_marker:
            if next_marker_pos > pos:
                block_text = content[pos:next_marker_pos].strip()
                if block_text:
                    blocks.append(("default", block_text))
            
            block_end = len(content)
            for m in markers:
                next_pos = content.find(m, next_marker_pos + len(next_marker))
                if next_pos != -1 and next_pos < block_end:
                    block_end = next_pos
            
            block_text = content[next_marker_pos + len(next_marker):block_end].strip()
            
            if next_marker.lower().startswith("thought"):
                thought_text, _ = parse_thought_action(block_text)
                block_text = thought_text
            elif next_marker.lower().startswith("action"):
                _, action_text = parse_thought_action(block_text)
                block_text = action_text
            
            block_type = next_marker.lower().replace(":", "")
            blocks.append((block_type, block_text))
            pos = block_end
        else:
            remaining = content[pos:].strip()
            if remaining:
                blocks.append(("default", remaining))
            break
    
    return blocks


def _render_blocks(blocks, role: str, final_answer_container):
    """
    Renders each block according to its type (thought, action, final answer, error, or default).
    """
    for block_type, text in blocks:
        if block_type == "final answer" and final_answer_container is not None:
            _render_final_answer_block(text, final_answer_container)
        
        _render_standard_block(block_type, text, role)


def _render_final_answer_block(text: str, final_answer_container):
    """
    Handles the special case for rendering the 'Final Answer' block, 
    including image extraction and formatting.
    """
    # 1. Create containers for the final answer and images
    answer_container, image_container = _create_answer_and_image_containers(final_answer_container)

    # 2. Parse or extract images from the text
    all_urls, processed_text = _parse_or_extract_images(text)

    # 3. Display the final answer
    _display_final_answer(answer_container, processed_text)

    # 4. Display images in a uniform grid
    _display_images(image_container, all_urls)


def _create_answer_and_image_containers(final_answer_container):
    """
    Creates two Streamlit containers: one for the final answer,
    and one for images.
    """
    answer_container = final_answer_container.container()
    image_container = final_answer_container.container()
    return answer_container, image_container


def _parse_or_extract_images(text: str):
    """
    Tries to parse `text` as a dictionary and extract image URLs.
    If parsing fails, it falls back to cleaning and extracting text + URLs.
    """
    try:
        if isinstance(text, dict):
            # Direct dictionary input
            all_urls = extract_image_urls_from_observation(text)
            processed_text = str(text)
        elif isinstance(text, str):
            try:
                # Try to parse as dictionary
                observation = ast.literal_eval(text)
                if isinstance(observation, dict):
                    all_urls = extract_image_urls_from_observation(observation)
                    processed_text = text
                else:
                    all_urls, processed_text = extract_and_clean_text(text)
            except:
                all_urls, processed_text = extract_and_clean_text(text)
        else:
            all_urls, processed_text = extract_and_clean_text(str(text))
    except Exception as e:
        print(f"Error in URL extraction: {e}")
        all_urls, processed_text = extract_and_clean_text(str(text))

    return all_urls, processed_text


def _clean_and_format_text(processed_text: str) -> str:
    """
    Calls the LLM to fix grammar, sentence structure, and spelling mistakes,
    returning the text as neat, easy-to-read markdown without italics.
    """
    gemini_client = initialize_genai_client()
    MODEL_ID: str = "gemini-2.0-flash-exp"

    # Updated prompt: only fix grammar, sentence structure, and spelling mistakes.
    prompt: str = f"""
Fix grammar, sentence structure, and spelling mistakes only. 
Return the text in neatly formatted markdown (DO NOT use italics). 
Escape dollar signs properly. 
Do not remove or add content. 
Strictly no placeholders for images like e.g., 'Image 2 displayed below' or [image] or [url], etc. 
Avoid saying Image 1, Image 2 etc.
DO NOT use italics in markdown.
Avoid hashtags.
Avoid saying things like "Okay, here's the corrected text:"

{processed_text}

IMPORTANT - Remove all hyperlinks to images.
    """

    response = generate_content(gemini_client, MODEL_ID, prompt).text
    return response


def _display_final_answer(answer_container, cleaned_text: str):
    """
    Displays the cleaned final answer within its container.
    """
    answer_container.markdown(
        f"""<div style='background-color:#FFFFFF; border-radius:12px; margin:24px 0; padding:30px; font-size:16px; line-height:1.8; color:#333; box-shadow:0 4px 12px rgba(0,0,0,0.05); border:1px solid #E0E0E0'>
            <h3 style='color:#186A3B; margin:0 0 20px 0; font-size:24px; font-weight:600'>Final Answer</h3>
            {cleaned_text}""",
        unsafe_allow_html=True
    )


def _display_images(image_container, all_urls):
    """
    Displays a list of image URLs in a uniform grid layout.
    If an image URL cannot be fetched, a placeholder image is displayed.
    """
    if all_urls:
        num_columns = 5
        cols = image_container.columns(num_columns)

        image_width = 500
        image_height = 500

        for idx, url in enumerate(all_urls):
            col_idx = idx % num_columns
            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        overflow: hidden;
                        height: {image_height}px;
                    ">
                        <img src="{url}"
                             onerror="this.onerror=null;this.src='./img/placeholder-image.png';"
                             style="
                                width: {image_width}px;
                                height: {image_height}px;
                                object-fit: cover;
                             " />
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def _render_standard_block(block_type: str, text: str, role: str):
    """
    Renders a single block of content (if it's not the final answer block).
    """
    style_map = {
        "thought": ("E6EEFF", "3498db", "Thought"),
        "action": ("F0E6FF", "6C3483", "Action"),
        "error": ("FFCCCC", "AA0000", "Error"),
        "default": ("FFFFFF", "95a5a6", role.capitalize())
    }
    
    bg_color, accent_color, label = style_map.get(block_type, style_map["default"])
    
    st.markdown(
        f"""<div style='background-color:#{bg_color}; border-radius:8px; margin:10px 0; padding:15px; font-size:15px; line-height:1.5; color:#2C3E50; border-left:4px solid #{accent_color}'>
            <strong style='color:#{accent_color};'>{label}:</strong>
            <div style='margin-top:8px'>{text}</div>
        </div>""",
        unsafe_allow_html=True
    )



def set_page_config_and_styles() -> None:
    """
    Sets the Streamlit page configuration and applies combined CSS styles
    from the TemplateLoader.
    """
    # Set the page configuration
    st.set_page_config(
        page_title="Agentic Search",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

    # Load and inject styles (no logic change)
    st.markdown(template_loader.get_combined_styles(), unsafe_allow_html=True)


def render_sidebar() -> int:
    """
    Renders the sidebar including the Google icon (if available) and
    a number input for maximum iterations.

    :return: The integer value from the max_iterations number input.
    """
    with st.sidebar:
        # Display Google icon if it exists
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)

        # Number input for max iterations
        max_iterations = st.number_input(
            "Max Iterations",
            min_value=1,
            max_value=30,
            value=10,
            step=1,
            help="Set how many reasoning steps the agent can perform."
        )

    return max_iterations


def display_header() -> None:
    """
    Displays the main title and subtitle at the top of the page.
    """
    st.markdown("<h1 class='main-title'>Agentic Search</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Navigating Knowledge with Intelligent AI Exploration</div>", unsafe_allow_html=True)


def handle_file_upload(uploaded_file: Optional[Any]) -> Tuple[Optional[str], str]:
    """
    Handles the file upload process for an image (if any),
    saves it locally in a 'tmp/uploads' directory with a unique filename.

    :param uploaded_file: The uploaded file object (or None).
    :return: A tuple (image_path, display_html) where:
             image_path is the path to the saved image or None,
             display_html is the HTML snippet to display the thumbnail (or the clip icon).
    """
    # If no file is uploaded, return clip icon HTML
    if uploaded_file is None:
        clip_icon_html = """
            <div class="clip-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                </svg>
            </div>
        """
        return None, clip_icon_html

    # Create 'tmp/uploads' directory if it doesn't exist
    if not os.path.exists('tmp/uploads'):
        os.makedirs('tmp/uploads', exist_ok=True)

    # Generate a unique filename based on timestamp and hash
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = abs(hash(uploaded_file.name))
    _, ext = os.path.splitext(uploaded_file.name)
    unique_filename = f"{timestamp}_{unique_id}{ext}"
    image_path = os.path.join('tmp/uploads', unique_filename)

    # Save the uploaded image
    with open(image_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Log the image upload
    logger.info(f"Image uploaded - Filename: {uploaded_file.name}, Saved as: {image_path}")

    # Prepare thumbnail display HTML with a remove button
    thumbnail_html = f"""
        <div class="thumbnail-wrapper">
            <img src="data:image/jpeg;base64,{base64.b64encode(uploaded_file.getvalue()).decode()}" 
                 class="thumbnail" alt="Uploaded image thumbnail"/>
            <div class="remove-thumbnail">×</div>
        </div>
    """
    return image_path, thumbnail_html


def handle_query_and_display_result(
    user_query: str,
    uploaded_file: Optional[Any],
    image_path: Optional[str],
    max_iterations: int
) -> None:
    """
    If the user clicked the 'Explore' button and has provided a query,
    this function runs the React Agent, displays the reasoning trace
    and the final answer, and handles cleanup of any uploaded image.

    :param user_query: The text input from the user.
    :param uploaded_file: The uploaded file object (None if not provided).
    :param image_path: The path to the uploaded image or None.
    :param max_iterations: The maximum number of iterations for the React Agent.
    """
    final_answer_container = st.container()

    # Prepare data for the React agent
    if uploaded_file is not None:
        query_data = {
            "text": user_query,
            "image_path": image_path
        }
        # Log multimodal input
        logger.info(f"Multimodal input received - Query: {user_query}, Image: {image_path}")
    else:
        query_data = {
            "text": user_query,
            "image_path": None
        }
        # Log text-only input
        logger.info(f"Text-only input received - Query: {user_query}")

    # Display the reasoning trace title
    st.markdown(
        """
        <h2 class='reasoning-title'>
            Reasoning Trace
        </h2>
        """,
        unsafe_allow_html=True
    )

    try:
        # Iterate through the agent's reasoning steps
        for iteration_count, data in enumerate(run_react_agent(query_data, max_iterations), start=1):
            st.markdown(
                f"""
                <div style='margin:24px 0 12px 0;'>
                    <span style='color:#333; font-size:14px; font-weight:500; 
                           text-transform:uppercase; letter-spacing:0.5px;'>
                        Iteration {iteration_count}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Display each message in the iteration
            for msg in data["messages"]:
                display_message(msg.role, msg.content, final_answer_container)

            # If the agent is done or we've reached max iterations, stop
            if data.get("done") or (iteration_count == max_iterations):
                break

    except Exception as e:
        # Display an error if something goes wrong
        st.error(f"An error occurred during processing: {str(e)}")
        logger.error(f"Error in run_react_agent: {str(e)}", exc_info=True)

    finally:
        # Cleanup the uploaded image if it exists
        if uploaded_file is not None and image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                logger.info(f"Cleaned up uploaded image: {image_path}")
            except Exception as e:
                logger.error(f"Error cleaning up uploaded image: {str(e)}")

