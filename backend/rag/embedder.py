import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def embed_text(text: str) -> list[float]:
    """
    Embed text using OpenAI text-embedding-3-small.
    Replaces the heavy sentence-transformers/PyTorch dependency (~2.5GB)
    with a lightweight API call. Cost: ~$0.02 per 1M tokens.
    """
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set. Returning zero vector.")
        return [0.0] * 1536  # text-embedding-3-small dimension

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"OpenAI embedding error: {e}")
        return [0.0] * 1536
