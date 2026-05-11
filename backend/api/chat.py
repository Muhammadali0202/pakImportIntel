from fastapi import APIRouter, Depends
from pydantic import BaseModel
from rag.vector_store import retrieve_chunks
from agents.router import AgentRouter
from agents.document_agent import DocumentAgent
from agents.chat_agent import ChatAgent
from agents.route_agent import RouteAgent
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Shipment
from utils.llm_client import call_llm
import os
import json

router = APIRouter()
agent_router = AgentRouter()
doc_agent = DocumentAgent()
chat_agent = ChatAgent()
route_agent = RouteAgent()

class ChatRequest(BaseModel):
    query: str
    user_id: str = "demo_user"

@router.post("/query")
def chat_query(payload: ChatRequest, db: Session = Depends(get_db)):
    # 1. Retrieve RAG chunks
    try:
        chunks = retrieve_chunks(payload.query, payload.user_id, n_results=3)
        context_text = "\n\n".join([chunk["text"] for chunk in chunks]) if chunks else ""
    except Exception as e:
        context_text = ""
    
    # 2. Route the intent
    target_agent = agent_router.route(payload.query)
    
    # 3. Call the appropriate agent
    if target_agent == "document_agent":
        response = doc_agent.process_query(payload.query, context_text)
    elif target_agent == "chat_agent":
        shipments = db.query(Shipment).all()
        shipment_data = [{"id": s.id, "status": s.status, "eta": s.eta, "location": s.current_location} for s in shipments]
        response = chat_agent.process_query(payload.query, shipment_data)
    elif target_agent == "duty_agent":
        # Request JSON from general LLM
        prompt = f"User Query: {payload.query}. Provide a structured JSON response about Pakistan Customs Duty."
        response = call_llm("You are a Pakistan Customs Duty expert. Always return JSON with 'answer', 'financial_metrics', and 'extracted_intel'.", prompt)
    elif target_agent == "route_agent":
        route_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'routes.json')
        try:
            with open(route_path, 'r', encoding='utf-8') as f:
                route_data = json.load(f)
        except Exception:
            route_data = {}
        response = route_agent.process_query(payload.query, route_data)
    else:
        response = json.dumps({"answer": "I'm sorry, I couldn't process that request."})
        
    # 4. Parse JSON response
    try:
        data = json.loads(response)
    except Exception:
        data = {"answer": response}
        
    return {
        **data,
        "agent_used": target_agent, 
        "context_used": bool(context_text)
    }
