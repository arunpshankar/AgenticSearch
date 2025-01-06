from src.config.setup import initialize_genai_client
from src.config.logging import logger
from google import genai
import time


def generate_content(client: genai.Client, model_id: str, prompt: str) -> str:
    """
    Generates content using the GenAI client and specified model.

    Args:
        client (genai.Client): The GenAI client.
        model_id (str): The model ID to use for generation.
        prompt (str): The prompt for content generation.

    Returns:
        str: The generated content.

    Raises:
        Exception: If content generation fails.
    """
    try:
        logger.info(f"Generating content using model: {model_id}")
        start_time = time.time()  # Start the timer
        response = client.models.generate_content(model=model_id, contents=prompt)
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time
        logger.info(f"Content generated successfully in {elapsed_time:.2f} seconds.")
        logger.info(f"Response: {response.text.strip()}")
        return response
    except Exception as e:
        logger.error("Failed to generate content.")
        try:
            logger.error(f"Partial response (if any): {response.text.strip()}")
        except NameError:
            logger.error("No response available due to an exception.")
        logger.error(f"Exception details: {e}")
        raise



if __name__ == "__main__":
    try:
        gemini_client: genai.Client = initialize_genai_client()

        MODEL_ID: str = "gemini-2.0-flash-exp"
        prompt: str = "What's the largest planet in our solar system?"

        # Generate content
        generate_content(gemini_client, MODEL_ID, prompt)
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")
