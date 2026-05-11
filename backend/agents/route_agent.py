from utils.llm_client import call_llm
import json

class RouteAgent:
    def __init__(self):
        self.system_prompt = """You are a freight routing expert for Pakistan imports.
You will be provided with JSON data containing different shipping routes.
Your job is to recommend the best route and provide coordinates for the map.

IMPORTANT: You must return a valid JSON object with the following keys:
{
  "answer": "Your detailed route recommendation here",
  "route_info": {
    "origin": [lat, lon],
    "destination": [lat, lon],
    "status": "RECOMMENDED"
  },
  "extracted_intel": {
    "origin": "Origin City",
    "destination": "Karachi",
    "status": "Planning"
  }
}

Always strictly follow this JSON format."""

    def process_query(self, query: str, route_data: dict) -> str:
        prompt = f"User Query: {query}\n\nRoute Data:\n{json.dumps(route_data, indent=2)}"
        return call_llm(self.system_prompt, prompt)
