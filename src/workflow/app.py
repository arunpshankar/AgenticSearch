from src.workflow.helper import display_message
from src.config.setup import GOOGLE_ICON_PATH
from src.utils.template import TemplateLoader
from src.agents.react import run_react_agent
from src.config.logging import logger
from typing import Optional
from typing import Tuple
from typing import Any 
import streamlit as st
import datetime
import base64
import os


template_loader = TemplateLoader()


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
    st.markdown("<div class='subtitle'>Discover Insights Through AI-Powered Exploration</div>", unsafe_allow_html=True)


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


def run() -> None:
    """
    Main function that sets up the Streamlit app, handles user input,
    displays the search components, and orchestrates the React Agent calls.
    """
    # Set page config and inject CSS
    set_page_config_and_styles()

    # Render the sidebar and get the max_iterations value
    max_iterations = render_sidebar()

    # Display header (main title + subtitle)
    display_header()

    # Create a container for the search components
    search_container = st.container()
    with search_container:
        st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

        # Main search input (user query)
        user_query = st.text_input(
            "Search or ask a question",
            key="explore_question",
            label_visibility="collapsed",
            placeholder="Ask anything...",
            help="Type your question here!"
        )

        # Hidden file uploader triggered by clip icon
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg'],
            key="hidden_uploader",
            label_visibility="collapsed"
        )

        # Handle file upload and display the appropriate icon/thumbnail
        image_path, display_html = handle_file_upload(uploaded_file)
        st.markdown(display_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Center the "Explore" button
    _, col2, _ = st.columns([6, 2, 6])
    with col2:
        search_clicked = st.button(
            "Explore",
            key="search_button",
            type="primary",
            help="Ask the Gemini React Agent"
        )

    # When user clicks "Explore" and has typed something
    if search_clicked and user_query.strip():
        handle_query_and_display_result(user_query, uploaded_file, image_path, max_iterations)


if __name__ == "__main__":
    run()
