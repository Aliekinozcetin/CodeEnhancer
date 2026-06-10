# client_factory.py — Ollama OpenAI-compat client wrapper
# Single responsibility: Returns (client, model_id) tuple when model key is provided.
# All Ollama connection details are isolated in this file.
# Other scripts only call get_client("qwen25coder_7b").

import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# ─── Model Registry ───────────────────────────────────────────────
# key: short name in the project (consistent with folder names)
# value: model tag in Ollama
MODEL_REGISTRY = {
    "qwen25coder_7b":      "qwen2.5-coder:7b",
    "mistral_7b":          "mistral:7b",
    "deepseek_coder_6_7b": "deepseek-coder:6.7b-instruct",
    "llama31_8b":          "llama3.1:8b",
    "gemma2_9b":           "gemma2:9b",
}

# ─── Ollama Base URL ───────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")


def get_client(model_key: str):
    """
    Returns the OpenAI-compat client and Ollama model ID based on the model key.

    Args:
        model_key: Short name in MODEL_REGISTRY.
                   Example: "qwen25coder_7b", "llama31_8b", "gemma2_9b"

    Returns:
        tuple: (OpenAI client, model_id string)

    Raises:
        ValueError: Unknown model key.
    """
    if model_key not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model: '{model_key}'. "
            f"Valid models: {list(MODEL_REGISTRY.keys())}"
        )

    model_id = MODEL_REGISTRY[model_key]

    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama does not require an API key, placeholder
    )

    return client, model_id


def test_connection(model_key: str) -> bool:
    """
    Tests the connection and model accessibility by sending a simple prompt to Ollama.

    Args:
        model_key: Model to be tested.

    Returns:
        True: Connection successful and model returned response.
        False: Connection or model access error.
    """
    try:
        client, model_id = get_client(model_key)
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "Say 'ok' and nothing else."}],
            max_tokens=5,
            temperature=0,
        )
        reply = response.choices[0].message.content.strip()
        return len(reply) > 0
    except Exception as e:
        print(f"[ERROR] {model_key} ({MODEL_REGISTRY.get(model_key, '?')}): {e}")
        return False


def list_available_models():
    """Lists all registered models and their accessibility status."""
    print(f"Ollama endpoint: {OLLAMA_BASE_URL}")
    print(f"{'Model Key':<20} {'Ollama Tag':<22} {'Status'}")
    print("-" * 55)
    for key, tag in MODEL_REGISTRY.items():
        status = "[OK] Accessible" if test_connection(key) else "[FAIL] Inaccessible"
        print(f"{key:<20} {tag:<22} {status}")


# ─── CLI: Tests all models if run directly ─────────
if __name__ == "__main__":
    list_available_models()
