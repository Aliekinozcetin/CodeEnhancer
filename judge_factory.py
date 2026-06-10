# judge_factory.py — OpenAI client factory for LLM Judge (GPT-4o-mini)
# Single responsibility: Connect with OpenAI API key and return (client, model_id).

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_judge_client():
    """
    Returns the GPT-4o-mini judge client and model ID.
    
    Returns:
        tuple: (OpenAI client instance, model_id string)
        
    Raises:
        ValueError: When the OpenAI API key is not found.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found in the .env file or environment variables. "
            "Please add your API key."
        )
    
    client = OpenAI(api_key=api_key)
    return client, "gpt-4o-mini"
