import os
import requests
from dotenv import load_dotenv

# Load environment variables if present
load_dotenv()

# Use BACKEND_URL from environment or fallback to localhost for local dev
BACKEND_URL = os.getenv("BACKEND_URL", "https://cargosense-backend-1060077955383.us-central1.run.app")

def get_shipments():
    try:
        response = requests.get(f"{BACKEND_URL}/api/shipments", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching shipments: {e}")
        return []

def estimate_duties(cif_value, origin="CN", product_hs_code="8517.13", is_filer=True):
    try:
        response = requests.post(f"{BACKEND_URL}/api/duties/estimate", json={
            "cif_value": cif_value,
            "origin": origin,
            "product_hs_code": product_hs_code,
            "is_filer": is_filer
        }, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error estimating duties: {e}")
        return None

def chat_query(query, context=None):
    try:
        response = requests.post(f"{BACKEND_URL}/api/chat/query", json={
            "query": query,
            "context": context
        }, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying chat: {e}")
        return None

def upload_document(file_bytes: bytes, filename: str, user_id: str = "demo_user"):
    """Upload a document to the backend for RAG ingestion."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/documents/upload",
            files={"file": (filename, file_bytes, "application/octet-stream")},
            params={"user_id": user_id},
            timeout=60  # OCR can be slow
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error uploading document: {e}")
        return None
