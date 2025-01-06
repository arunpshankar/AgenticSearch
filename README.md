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

Agentic Search integrates a robust toolset, including:

- **Wikipedia API**: Fetch summaries of topics.
- **SerpAPI**: Perform Google search, image search, and trends analysis.
- **Public APIs**: Retrieve facts, jokes, and other informative content.
- **Custom Tools**: Extend functionality with Gemini 2.0 for text-image reasoning.

#

## Contribution

We welcome contributions! Please fork this repository and submit a pull request with detailed descriptions of your updates.

#

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.