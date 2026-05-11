import chromadb
import sys
import os

# Ensure config can be imported when running scripts directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import settings
    chroma_path = settings.chroma_path
except ImportError:
    chroma_path = "./chroma_db"

from rag.embedder import embed_text

# Initialize ChromaDB client
client = chromadb.PersistentClient(path=chroma_path)
collection = client.get_or_create_collection(
    name="shipment_documents_v3",
    metadata={"hnsw:space": "cosine"}
)

def store_chunks(chunks: list[str], metadata: dict):
    """Save text chunks and their embeddings to ChromaDB."""
    if not chunks:
        return
        
    embeddings = [embed_text(chunk) for chunk in chunks]
    
    doc_id = metadata.get("doc_id", "unknown_doc")
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    
    metadatas = [metadata.copy() for _ in chunks]
    for i, meta in enumerate(metadatas):
        meta["chunk_index"] = i
        
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

def retrieve_chunks(query: str, user_id: str, n_results: int = 5) -> list[dict]:
    """Perform a similarity search in ChromaDB."""
    query_embedding = embed_text(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"user_id": user_id}
    )
    
    retrieved_chunks = []
    
    if results and results.get("documents") and len(results["documents"]) > 0:
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results.get("distances", [[0]*len(docs)])[0]
        
        for i in range(len(docs)):
            retrieved_chunks.append({
                "text": docs[i],
                "metadata": metas[i],
                "distance": distances[i]
            })
            
    return retrieved_chunks
