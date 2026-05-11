import os
import uuid
import tempfile
import logging
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from rag.parser import parse_pdf
from rag.chunker import chunk_text
from rag.vector_store import store_chunks
from agents.document_agent import DocumentAgent

router = APIRouter()
logger = logging.getLogger(__name__)
doc_agent = DocumentAgent()

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), user_id: str = "demo_user"):
    """
    Accepts a PDF or image file, parses it, chunks it, embeds it,
    and stores it in ChromaDB so it can be retrieved by the chat agent.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    # Save upload to a temp file so parsers can read it from disk
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Parse text from the file
        if ext == ".pdf":
            text = parse_pdf(tmp_path)
        else:
            # For image files (invoices, BoL scans) use EasyOCR directly
            try:
                import easyocr
                reader = easyocr.Reader(['en'])
                result = reader.readtext(tmp_path, detail=0)
                text = " ".join(result)
            except ImportError:
                raise HTTPException(status_code=501, detail="EasyOCR not installed. Only PDF uploads are supported on this server.")

        if not text.strip():
            raise HTTPException(status_code=422, detail="No text could be extracted from this document.")

        # ---- AUTO EXTRACTION ----
        # Ask DocumentAgent to extract intelligence from the full text immediately
        raw_intel = doc_agent.process_query("Extract all shipment metadata (origin, destination, hs code, value, consignee, etc.)", text[:4000]) # Use first 4000 chars for extraction
        try:
            extracted_data = json.loads(raw_intel)
        except:
            extracted_data = {}

        # Chunk → embed → store into ChromaDB
        chunks = chunk_text(text)
        doc_id = str(uuid.uuid4())
        metadata = {
            "user_id": user_id,
            "filename": file.filename,
            "doc_id": doc_id
        }
        store_chunks(chunks, metadata)

        logger.info(f"Stored {len(chunks)} chunks from '{file.filename}' for user '{user_id}'")
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_stored": len(chunks),
            "doc_id": doc_id,
            "extracted_intel": extracted_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    finally:
        # Always clean up temp file
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
