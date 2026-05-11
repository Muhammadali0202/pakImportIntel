import requests
import json
import time
import subprocess
import os

print("Starting server...")
# Start the uvicorn server in a subprocess
env = os.environ.copy()
# Assume venv is activated or we use the python executable directly
process = subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--port", "8000"], cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for server to start
time.sleep(5)

BASE_URL = "http://localhost:8000/api"

try:
    print("\n--- Testing GET /api/shipments ---")
    r = requests.get(f"{BASE_URL}/shipments")
    print(f"Status: {r.status_code}")
    print(f"Response: {len(r.json())} shipments found.")

    print("\n--- Testing POST /api/duties/estimate ---")
    payload = {
        "cif_value": 10000,
        "origin": "China",
        "product_hs_code": "8517.13"
    }
    r = requests.post(f"{BASE_URL}/duties/estimate", json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response snippet: {r.text[:100]}...")

    print("\n--- Testing POST /api/chat/query (Tracking) ---")
    r = requests.post(f"{BASE_URL}/chat/query", json={"query": "Where is my shipment COSCO HARMONY?"})
    print(f"Status: {r.status_code}")
    try:
        print(f"Agent used: {r.json().get('agent_used')}")
        print(f"Response snippet: {r.json().get('response')[:100]}...")
    except:
        print(r.text)

    print("\n--- Testing POST /api/chat/query (Route) ---")
    r = requests.post(f"{BASE_URL}/chat/query", json={"query": "Compare air vs sea freight from China."})
    print(f"Status: {r.status_code}")
    try:
        print(f"Agent used: {r.json().get('agent_used')}")
        print(f"Response snippet: {r.json().get('response')[:100]}...")
    except:
        print(r.text)

finally:
    print("\nShutting down server...")
    process.terminate()
