from src.config.setup import initialize_genai_client
from src.config.logging import logger
from pathlib import Path
from PIL import Image


def generate_multimodal_content(prompt: str, image_path: str) -> str:
    """
    Generates content from a text prompt and local image.
    
    Args:
        prompt (str): Text prompt for content generation
        image_path (str): Path to the image file
    
    Returns:
        str: Generated content text
    """
    try:
        client = initialize_genai_client()
        image = Image.open(Path(image_path))
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[image, prompt]
        )
        return response.text
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise

if __name__ == "__main__":
    try:
        content = generate_multimodal_content(
            "Write a short and engaging blog post based on this picture.",
            "./tmp/uploads/sample.jpg"
        )
        print(content)
    except Exception as e:
        print(f"Error: {e}")