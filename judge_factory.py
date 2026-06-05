# judge_factory.py — OpenAI client factory for LLM Judge (GPT-4o-mini)
# Tek sorumluluk: OpenAI API key ile baglanip (client, model_id) donmek.

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_judge_client():
    """
    GPT-4o-mini judge client ve model adini doner.
    
    Returns:
        tuple: (OpenAI client instance, model_id string)
        
    Raises:
        ValueError: OpenAI API anahtari bulunamadiginda.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY .env dosyasinda veya ortam degiskenlerinde bulunamadi. "
            "Lutfen API anahtarinizi ekleyin."
        )
    
    client = OpenAI(api_key=api_key)
    return client, "gpt-4o-mini"
