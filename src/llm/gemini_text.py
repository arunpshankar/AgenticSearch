import time
from src.config.setup import initialize_genai_client
from src.config.logging import logger
from google import genai

RETRYABLE_STATUS_CODES = [400, 500]
MAX_RETRIES = 5

def generate_content(client: genai.Client, model_id: str, prompt: str) -> str:
    """
    Generates content using the GenAI client and specified model with up to 5 retries
    (exponential backoff) if certain status codes (e.g., 400, 500) are encountered.

    Args:
        client (genai.Client): The GenAI client.
        model_id (str): The model ID to use for generation.
        prompt (str): The prompt for content generation.

    Returns:
        str: The generated content.

    Raises:
        Exception: If content generation fails after retries or a non-retryable error occurs.
    """
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            logger.info(f"Generating content using model: {model_id}, Attempt: {attempt + 1}")
            start_time = time.time()  # Start the timer
            response = client.models.generate_content(model=model_id, contents=prompt)
            end_time = time.time()  # End the timer
            elapsed_time = end_time - start_time  # Calculate elapsed time

            logger.info(f"Content generated successfully in {elapsed_time:.2f} seconds.")
            logger.info(f"Response: {response.text.strip()}")
            return response

        except Exception as e:
            status_code = getattr(e, "status_code", None)
            logger.error(f"Attempt {attempt + 1} failed. Error code: {status_code}, Exception: {e}")

            # Retry if we hit one of our "retryable" status codes
            if status_code in RETRYABLE_STATUS_CODES:
                logger.error("Retryable error encountered; applying exponential backoff.")
                time.sleep(2 ** attempt)
                attempt += 1
            else:
                # Non-retryable error or unknown status code; log partial response if any, then raise
                logger.error("Non-retryable error or unknown status code. Aborting.")
                try:
                    logger.error(f"Partial response (if any): {response.text.strip()}")
                except NameError:
                    logger.error("No response available due to an exception.")
                raise

    logger.error(f"Failed to generate content after {MAX_RETRIES} attempts.")
    try:
        logger.error(f"Partial response (if any): {response.text.strip()}")
    except NameError:
        logger.error("No response available due to an exception.")
    raise Exception("Max retries reached. Content generation failed.")

if __name__ == "__main__":
    try:
        gemini_client: genai.Client = initialize_genai_client()

        MODEL_ID: str = "gemini-2.0-flash-exp"
        prompt: str = "What's the largest planet in our solar system?"

        # Generate content
        generate_content(gemini_client, MODEL_ID, prompt)
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")
