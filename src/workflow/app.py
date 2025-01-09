from src.config.logging import logger
from src.workflow.helper import *
import streamlit as st


def run() -> None:
    """
    Main function that sets up the Streamlit app, handles user input,
    displays the search components, and orchestrates the React Agent calls.
    """
    logger.info("Starting Streamlit application.")

    # Set page config and inject CSS
    logger.info("Setting up page configuration and styles.")
    set_page_config_and_styles()

    # Render the sidebar and get the max_iterations value
    logger.info("Rendering the sidebar for user input.")
    max_iterations = render_sidebar()

    # Display header (main title + subtitle)
    logger.info("Displaying header section.")
    display_header()

    # Create a container for the search components
    logger.info("Setting up the search container.")
    search_container = st.container()
    with search_container:
        st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

        # Main search input (user query)
        logger.info("Rendering the main search input field.")
        user_query = st.text_input(
            "Search or ask a question",
            key="explore_question",
            label_visibility="collapsed",
            placeholder="Ask anything...",
            help="Type your question here!"
        )

        # Hidden file uploader triggered by clip icon
        logger.info("Rendering the file uploader component.")
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg'],
            key="hidden_uploader",
            label_visibility="collapsed"
        )

        # Handle file upload and display the appropriate icon/thumbnail
        logger.info("Handling file upload, if any.")
        image_path, display_html = handle_file_upload(uploaded_file)
        st.markdown(display_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Center the "Explore" button
    _, col2, _ = st.columns([6, 2, 6])
    with col2:
        logger.info("Rendering the Explore button.")
        search_clicked = st.button(
            "Explore",
            key="search_button",
            type="primary",
            help="Ask the Gemini React Agent"
        )

    # When user clicks "Explore" and has typed something
    if search_clicked and user_query.strip():
        logger.info(f"Explore button clicked with query: {user_query.strip()}")
        handle_query_and_display_result(user_query, uploaded_file, image_path, max_iterations)


if __name__ == "__main__":
    logger.info("Running the main function.")
    run()
