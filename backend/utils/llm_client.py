import os
import logging
from dotenv import load_dotenv
from config import settings

# Explicitly load .env so the key is available even before uvicorn sets env vars
load_dotenv()

logger = logging.getLogger(__name__)

def call_llm(system_prompt: str, user_message: str) -> str:
    """Wrapper to call the LLM (using OpenAI API). Client is created lazily."""
    api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        logger.warning("OPENAI_API_KEY not set. Returning fallback response.")
        return "AI response unavailable: No API key configured. Please set OPENAI_API_KEY in your .env file."

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=settings.llm_model or "gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return f"Error connecting to LLM: {str(e)}"
