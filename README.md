# Agentic Search

**Agentic Search** is an advanced AI-powered framework that utilizes **Gemini 2.0** and a ReAct agent to perform complex searches and deliver detailed, cohesive answers. By synthesizing data from multiple APIs and leveraging a dynamic tool registry, it provides precise and scalable solutions for intricate queries.

![Agentic Search Overview](./img/agentic-search-1.png)

#

## Key Features

- **Gemini 2.0 Integration**: Leverages Gemini 2.0's natural language understanding and multimodal reasoning capabilities.
- **ReAct Agent Framework**: Implements the ReAct framework to enable iterative reasoning and decision-making for complex tasks.
- **Dynamic Tool Registry**: Integrates a wide range of tools, from Wikipedia search to Google Trends, to expand functionality.
- **Multimodal Support**: Handles text and image-based inputs for enriched query responses.
- **Streamlined Interface**: Built with a clean, interactive UI powered by Streamlit for user-friendly interactions.

#

## Installation

To get started, clone this repository and install the required dependencies:

```bash
git clone <repository_url>
cd Agentic-Search
pip install --upgrade pip
pip install -r requirements.txt
```

#

## Setup

Set the required environment variables:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PYTHONPATH:.
```

Ensure you have the necessary API keys (e.g., SerpAPI) and other credentials in your configuration.

#

## Usage

1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
2. **Provide Your Query**:
   Enter your search query or upload an image via the interface.
3. **View Results**:
   Interact with the ReAct agent's reasoning trace and receive comprehensive answers.

#

## Examples of Use

- Explore historical or real-time data using integrated APIs.
- Perform multimodal reasoning with text and image inputs.
- Generate insights from structured and unstructured data sources.

#

## Tools and APIs

Agentic Search integrates a wide range of tools from `registry.py`, enabling diverse functionalities:

- **Wikipedia Tools**:
  - `get_wiki_search_results`: Fetch summaries and metadata from Wikipedia.

- **Facts and Trivia**:
  - `get_cat_fact`: Retrieve a random cat fact.
  - `get_multiple_cat_facts`: Fetch multiple cat facts.
  - `get_cat_breeds`: Retrieve a list of cat breeds.
  - `get_random_joke`: Fetch a random joke.
  - `get_ten_random_jokes`: Retrieve ten random jokes.
  - `get_random_joke_by_type`: Fetch a random joke of a specific type.
  - `get_trivia_questions`: Retrieve trivia questions.

- **Animal Images**:
  - `get_random_dog_image`: Fetch a random dog image.
  - `get_multiple_dog_images`: Retrieve multiple random dog images.
  - `get_random_dog_breed_image`: Fetch an image of a specific dog breed.
  - `get_random_fox_image`: Fetch a random fox image.

- **Demographic Predictions**:
  - `get_predicted_age_by_name`: Predict age based on a name.
  - `get_gender_by_name`: Predict gender based on a name.
  - `get_nationality_by_name`: Predict nationality based on a name.

- **Location and Public Data**:
  - `get_zip_info`: Retrieve location data for U.S. ZIP codes.
  - `get_public_ip`: Fetch the public IP address of the requester.
  - `get_iss_location`: Get the current location of the International Space Station.

- **Google and SerpAPI Tools**:
  - `get_google_search_results`: Perform a Google search.
  - `get_google_image_search_results`: Fetch Google Images search results.
  - `get_google_news_search`: Perform a Google News search.
  - `get_google_maps_search`: Search for places using Google Maps.
  - `get_google_maps_place`: Retrieve details of a specific place.
  - `get_google_jobs_search`: Perform a Google Jobs search.
  - `get_google_shopping_search`: Fetch Google Shopping results.
  - `get_google_trends_interest_over_time`: Retrieve Google Trends interest-over-time data.
  - `get_google_trends_compared_breakdown`: Fetch compared breakdown data for multiple queries.
  - `get_google_trends_interest_by_region`: Retrieve Google Trends interest-by-region data.
  - `get_google_local_basic_search`: Perform a local business search.
  - `get_google_play_query_search`: Search for apps in the Google Play Store.
  - `get_google_events_basic_search`: Retrieve event details from Google.
  - `get_google_videos_basic_search`: Perform a Google Videos search.
  - `get_google_finance_basic_search`: Fetch Google Finance data.
  - `get_google_finance_currency_exchange`: Retrieve exchange rate data for currency pairs.

- **Third-Party APIs**:
  - `get_walmart_basic_search`: Search for products on Walmart.
  - `get_artwork_data`: Fetch artwork data from the Art Institute of Chicago.
  - `get_lyrics`: Retrieve song lyrics.
  - `get_google_trends_interest_over_time`: Fetch Google Trends interest-over-time data.

- **Multimodal Reasoning**:
  - `get_multimodal_reasoning`: Perform reasoning based on both text and image inputs.

This comprehensive tool registry enables Agentic Search to address a wide variety of user queries.

#

## Contribution

We welcome contributions! Please fork this repository and submit a pull request with detailed descriptions of your updates.

#

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.