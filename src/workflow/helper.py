from src.config.setup import initialize_genai_client
from src.llm.gemini_text import generate_content
from src.config.logging import logger
from typing import Dict
from typing import List 
import streamlit as st 
import json 
import ast
import re


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

    return image_urls


def extract_and_clean_text(text: str) -> tuple[list[str], str]:
    """
    Extracts image URLs and cleans up the text by removing image references,
    including URLs with "URL:", "url:", and hyperlinks. Removes floating or broken brackets,
    HTTP/HTTPS URLs, patterns like [pattern] or (pattern), and adds breaklines for readability.
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
        urls = [url for url in urls if not (url in seen or seen.add(url))]
        
        # Clean the text
        processed_text = text
        
        # Remove patterns like [pattern] or (pattern)
        processed_text = re.sub(r'\[(.*?)\]', r'\1', processed_text)  # Remove square brackets
        processed_text = re.sub(r'\((.*?)\)', r'\1', processed_text)  # Remove parentheses
        
        # Remove broken or floating brackets
        processed_text = re.sub(r'\[', '', processed_text)  # Remove stray '['
        processed_text = re.sub(r'\]', '', processed_text)  # Remove stray ']'
        processed_text = re.sub(r'\(', '', processed_text)  # Remove stray '('
        processed_text = re.sub(r'\)', '', processed_text)  # Remove stray ')'
        
        # Remove HTTP/HTTPS URLs from the text
        processed_text = re.sub(r'https?://[^\s\]\)]+', '', processed_text)
        
        # Remove generic image references
        processed_text = re.sub(r'\[Image[^\]]*?\]', '', processed_text)
        
        # Remove URLs with "URL:", "url:" prefixes
        processed_text = re.sub(r'(URL|url):\s*\S+', '', processed_text)
        
        # Remove hyperlinks
        processed_text = re.sub(r'<a\s+href=[\'"]?([^\'" >]+)[\'"]?>.+?</a>', '', processed_text)
        
        # Add breaklines for readability
        processed_text = re.sub(r'(?<=[.!?]) ', '\n', processed_text)  # Add newline after end of sentences
        processed_text = re.sub(r'(?<=:)', '\n', processed_text)       # Add newline after colon

        # Clean up extra whitespace
        processed_text = re.sub(r'\s+', ' ', processed_text).strip()

        return urls, processed_text

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

    # 3. Process bold markdown formatting
    processed_text = _apply_bold_formatting(processed_text)

    # 4. Clean and format the text using the LLM (fix grammar, sentence structure, spelling ONLY)
    cleaned_text = _clean_and_format_text(processed_text)

    # 5. Display the final answer
    _display_final_answer(answer_container, cleaned_text)

    # 6. Display images in a uniform grid
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


def _apply_bold_formatting(processed_text: str) -> str:
    """
    Applies bold formatting for any markdown `*...*` and `**...**` patterns,
    using <b> tags.
    """
    # 1. Apply bold formatting for double asterisks first
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', processed_text)

    # 2. Apply bold formatting for single asterisks afterward
    processed_text = re.sub(r'\*(.*?)\*', r'<b>\1</b>', processed_text)
    return processed_text


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
If there are images, mention them as "... are shown below." 
Strictly no placeholders for images like e.g., 'Image 2 displayed below' or [image] or [url], etc. 
Avoid saying Image 1, Image 2 etc.
DO NOT use italics in markdown.
Avoid hashtags.
Avoid saying things like "Okay, here's the corrected text:"

{processed_text}
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
                        <img src="{url}" style="
                            width: {image_width}px; 
                            height: {image_height}px; 
                            object-fit: cover; 
                        "> 
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
