# Agentic Search

**Agentic Search** is an advanced AI-powered framework utilizing **Gemini 2.0** and a ReAct agent to perform complex searches and deliver detailed, cohesive answers. By synthesizing data from multiple APIs and leveraging a dynamic tool registry, it provides precise and scalable solutions for intricate queries.

![Agentic Search Overview](./img/agentic-search-1.png)

# Key Features

- **Gemini 2.0 Integration**: Leverages Gemini 2.0's advanced natural language understanding and multimodal reasoning capabilities.  
- **ReAct Agent Framework**: Implements the ReAct framework for iterative reasoning and decision-making in complex tasks.  
- **Dynamic Tool Registry**: Seamlessly integrates tools, including Wikipedia search and Google Trends, to expand functionality.  
- **Multimodal Support**: Handles both text and image-based inputs to enrich query responses.  
- **Streamlined Interface**: Built with a clean and interactive UI using Streamlit for intuitive user interactions.

# Prerequisites

1. Create a folder named `credentials`.  
2. Inside the folder, create a `.yml` file containing API keys for Google and SerpAPI as shown below:  
   ```yaml
   GOOGLE_API_KEY: xxxxxxxxx
   SERP_API_KEY: xxxxxx
   ```

# Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/arunpshankar/AgenticSearch.git
cd Agentic-Search

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

# Setup

Set the necessary environment variables:

```bash
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PYTHONPATH:.
```

Ensure your `credentials` folder contains the required API keys.

# Usage

1. **Run the Application**:  
   Launch the Agentic Search Streamlit app:  
   ```bash
   streamlit run src/workflow/app.py
   ```

2. **Provide Your Query**:  
   Enter your search query or upload an image via the interface.  

3. **View Results**:  
   Interact with the ReAct agent's reasoning trace and receive detailed, accurate answers.

# Examples of Use

- **Example 1**: Conduct a search to retrieve Wikipedia data.  
- **Example 2**: Perform Google Trends analysis for multiple keywords.  
- **Example 3**: Use multimodal reasoning to analyze text and image inputs.

# Tools and APIs

Agentic Search integrates a variety of tools defined in `registry.py`, enabling diverse functionalities:

### Wikipedia Tools  
- **`get_wiki_search_results`**: Fetch summaries and metadata from Wikipedia.

### Facts and Trivia  
- **`get_cat_fact`**, **`get_multiple_cat_facts`**: Retrieve one or multiple cat facts.  
- **`get_random_joke`**, **`get_ten_random_jokes`**: Fetch random jokes.  
- **`get_trivia_questions`**: Retrieve trivia questions.

### Animal Images  
- **`get_random_dog_image`**: Fetch a random dog image.  
- **`get_random_fox_image`**: Fetch a random fox image.

### Demographic Predictions  
- **`get_predicted_age_by_name`**: Predict age based on a name.  
- **`get_gender_by_name`**: Predict gender based on a name.

### Google and SerpAPI Tools  
- **`get_google_search_results`**: Perform a Google search.  
- **`get_google_trends_interest_over_time`**: Fetch Google Trends interest-over-time data.  
- **`get_google_maps_place`**: Retrieve details of a specific place.

### Third-Party APIs  
- **`get_walmart_basic_search`**: Search for products on Walmart.  
- **`get_lyrics`**: Retrieve song lyrics.

### Multimodal Reasoning  
- **`get_multimodal_reasoning`**: Perform reasoning using text and image inputs.

This comprehensive tool registry allows Agentic Search to address diverse and intricate queries effectively.

# Contribution

We welcome contributions! Fork this repository and submit a pull request with detailed descriptions of your updates.

# License

This project is licensed under the MIT License. See the `LICENSE` file for details.  