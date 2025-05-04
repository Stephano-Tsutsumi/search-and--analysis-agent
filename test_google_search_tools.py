import os
from dotenv import load_dotenv
from rich import print
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel, OpenAIModelSettings
from tools import GoogleSearchTool

# Load environment variables from .env file
load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')

google_search_agent = Agent(
    name='GoogleSearchAgent',
    model=OpenAIModel('gpt-4o-mini'),
    model_settings=OpenAIModelSettings(
        max_tokens=8400,
        temperature=0.1,
        api_key=api_key # Get API key from environment
    ),
    tools=[GoogleSearchTool.google_search]
)

response = google_search_agent.run_sync('search for the best 20 coffee shop in San Francisco. Exclude YouTube as the source')
print(response.output)