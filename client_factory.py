# client_factory.py — Ollama OpenAI-compat client wrapper
# Tek sorumluluk: model key verilince (client, model_id) tuple döner.
# Tüm Ollama bağlantı detayları bu dosyada izole edilir.
# Diğer scriptler sadece get_client("qwen25coder_7b") çağırır.

import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# ─── Model Registry ───────────────────────────────────────────────
# key: projedeki kısa ad (klasör adlarıyla tutarlı)
# value: Ollama'daki model tag'i
MODEL_REGISTRY = {
    "qwen25coder_7b": "qwen2.5-coder:7b",
    "llama31_8b":     "llama3.1:8b",
    "gemma2_9b":      "gemma2:9b",
}

# ─── Ollama Base URL ───────────────────────────────────────────────
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")


def get_client(model_key: str):
    """
    Model key'e göre OpenAI-compat client ve Ollama model adını döner.

    Args:
        model_key: MODEL_REGISTRY'deki kısa ad.
                   Örnek: "qwen25coder_7b", "llama31_8b", "gemma2_9b"

    Returns:
        tuple: (OpenAI client, model_id string)

    Raises:
        ValueError: Bilinmeyen model key.
    """
    if model_key not in MODEL_REGISTRY:
        raise ValueError(
            f"Bilinmeyen model: '{model_key}'. "
            f"Geçerli modeller: {list(MODEL_REGISTRY.keys())}"
        )

    model_id = MODEL_REGISTRY[model_key]

    client = OpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="ollama",  # Ollama API key gerektirmez, placeholder
    )

    return client, model_id


def test_connection(model_key: str) -> bool:
    """
    Ollama'ya basit bir prompt göndererek bağlantıyı ve modelin
    erişilebilirliğini test eder.

    Args:
        model_key: Test edilecek model.

    Returns:
        True: Bağlantı başarılı ve model yanıt döndü.
        False: Bağlantı veya model erişim hatası.
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
    """Kayıtlı tüm modelleri ve erişilebilirlik durumlarını listeler."""
    print(f"Ollama endpoint: {OLLAMA_BASE_URL}")
    print(f"{'Model Key':<20} {'Ollama Tag':<22} {'Durum'}")
    print("-" * 55)
    for key, tag in MODEL_REGISTRY.items():
        status = "[OK] Erisilebilir" if test_connection(key) else "[FAIL] Erisilemiyor"
        print(f"{key:<20} {tag:<22} {status}")


# ─── CLI: Doğrudan çalıştırılırsa tüm modelleri test eder ─────────
if __name__ == "__main__":
    list_available_models()
