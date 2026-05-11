from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from api import shipments, shippo_routes, chat, duties, documents
from db.database import engine, Base
from db.seed_data import seed_shipments, seed_hscodes
from services.aisstream_service import connect_ais_stream

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create DB tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")
    seed_shipments()
    seed_hscodes()
    
    # Start AISStream background task
    asyncio.create_task(connect_ais_stream())
    
    yield
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(title="Pakistan Import Intelligence API", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], 
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(shipments.router, prefix="/api/shipments", tags=["Shipments"])
app.include_router(shippo_routes.router, prefix="/api/shippo", tags=["Shippo"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(duties.router, prefix="/api/duties", tags=["Duties"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Pakistan Import Intelligence"}
