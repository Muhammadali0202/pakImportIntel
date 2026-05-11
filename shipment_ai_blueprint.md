# 🚢 PAKISTAN IMPORT INTELLIGENCE PLATFORM
## Complete Hackathon Implementation Blueprint
### AI-Powered Shipment & Customs Intelligence for Pakistani SMEs

> **Team:** 3 Members | **Time:** 7 Hours | **Stack:** FastAPI + Streamlit + ChromaDB + Claude/Gemini API

---

# TABLE OF CONTENTS

1. Product Understanding
2. Hackathon MVP Scope
3. System Architecture
4. Multi-Agent Architecture
5. RAG Pipeline
6. APIs & Data Sources
7. Database Design
8. Backend Architecture
9. Frontend Architecture
10. Cloud & Deployment
11. Team Division
12. 7-Hour Execution Roadmap
13. Prompt Engineering
14. Demo Strategy
15. Future Scalability
16. Risks & Failure Points

---

# SECTION 1 — PRODUCT UNDERSTANDING

## Problem Statement

Pakistani importers and SMEs operate in one of the world's most opaque and fragmented import ecosystems. A shop owner in Karachi importing electronics from Shenzhen has NO reliable way to:

- Know where their container actually is right now
- Predict if it will be delayed at Port Qasim or Karachi Port
- Understand what duties they will actually owe (SRB, FBR, customs duty, regulatory duty, additional customs duty)
- Interpret the documents in their hands (Bill of Lading, commercial invoice, packing list, LC)
- Compare whether air freight via Dubai makes more sense than sea freight via Colombo
- Get answers in plain Urdu/English without hiring an expensive customs agent

This is not a marginal problem. Pakistan imports roughly **$55–65 billion USD annually**. The vast majority of this is handled by SMEs and informal traders who navigate this with spreadsheets, WhatsApp, and guesswork.

## User Personas

### Persona 1: Ahmed — Electronics Importer, Karachi
- Imports Android phones and accessories from Shenzhen monthly
- Spends hours calling freight forwarders to get shipment updates
- Has been hit with unexpected duties 3 times this year
- Can't read English documents clearly
- Needs: real-time status, duty calculator, document Q&A

### Persona 2: Fatima — Textile Wholesaler, Lahore
- Imports fabric from China and UAE
- Loses money on delayed shipments due to seasonal demand
- Doesn't understand HS code classification
- Needs: ETA prediction, route comparison, HS code lookup

### Persona 3: Asad — Logistics Manager, SME, Faisalabad
- Manages 10–15 shipments simultaneously
- Drowning in paperwork — BOL, customs forms, invoices
- Can't extract data from PDFs easily
- Needs: document intelligence, multi-shipment dashboard, alerts

### Persona 4: Raza — Customs Clearing Agent
- Helps multiple clients with customs declarations
- Needs fast lookup of duty rates, SRO notifications, HS codes
- Needs: intelligent knowledge base, regulatory search, document Q&A

## Market Need

| Factor | Data |
|---|---|
| Pakistan annual imports | ~$60B USD |
| SMEs as % of importers | ~85% |
| Average customs delay | 3–14 days |
| Cost of delay (avg shipment) | $500–$5,000 |
| Customs agents average fee | 1–3% of shipment value |
| Digital penetration in logistics | <15% |

No dominant AI-native product exists for Pakistani importers. Existing tools (TradeKey, CargoStar) are basic directories. There is a genuine blue ocean.

## Core Value Proposition

**"Your 24/7 AI customs expert and shipment tracker — built for Pakistani importers."**

1. Upload your documents → AI understands them instantly
2. Ask questions in plain language → get grounded, accurate answers
3. Track all shipments in one place → never miss an update
4. Know your duties before goods arrive → no more surprises
5. Get route recommendations backed by real data

## What Makes This Unique

- **Pakistan-specific** — trained on FBR duty tables, SRO notifications, Pakistani port data
- **Document-native** — RAG over YOUR documents, not generic knowledge
- **Multi-modal** — handles PDFs, images of documents, text queries
- **Explainable** — AI shows WHY it recommends something, citing sources
- **Local context** — understands Karachi Port, Port Qasim, Torkham, Wagah border

---

# SECTION 2 — HACKATHON MVP SCOPE

## The 3-Layer MVP Strategy

### Layer 1 — MUST BUILD (Core Demo) — 4 hours
These are non-negotiable. The demo dies without them.

| Feature | Why Critical |
|---|---|
| AI Chat with RAG | The "wow" moment — upload doc, ask questions |
| Document Upload + Parsing | Enables the RAG pipeline |
| Duty Estimator | Concrete, useful, demos well |
| Shipment Dashboard (mocked) | Visual anchor for the demo |
| Route Comparison (AI-generated) | High-value feature, purely AI |

### Layer 2 — SHOULD BUILD (Demo Enhancers) — 2 hours
These make the demo richer but can be mocked if needed.

| Feature | Mock Strategy |
|---|---|
| Live Shipment Tracking | Use hardcoded JSON with realistic data |
| ETA Prediction | Use rule-based logic + AI explanation |
| Customs Risk Analysis | AI-generated from document context |
| Multi-shipment View | Static cards with realistic data |

### Layer 3 — EXCLUDE FROM MVP
Do NOT build these in 7 hours. Mention in future scope only.

- Real carrier API integrations (too complex, rate-limited)
- User authentication system (overkill for demo)
- Multi-user isolation (single-user demo is fine)
- Mobile app
- Urdu NLP fine-tuning
- Real-time port congestion feeds
- ERP integrations
- Payment processing

## Realistic MVP Feature Set

```
MVP = 
  AI Chat (RAG over uploaded docs)          ✅ BUILD
  + Document Upload & Parse                  ✅ BUILD
  + Duty/Tax Estimator                       ✅ BUILD  
  + Shipment Dashboard (mocked data)         ✅ BUILD
  + Route Comparison (AI reasoning)          ✅ BUILD
  + Customs Knowledge Q&A                    ✅ BUILD
  + Basic Analytics Cards                    ✅ BUILD
  
  Live tracking APIs                         ❌ MOCK
  User auth/login                            ❌ SKIP
  Real freight pricing APIs                  ❌ MOCK
  Urdu language support                      ❌ SKIP (mention in pitch)
```

---

# SECTION 3 — SYSTEM ARCHITECTURE

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER LAYER                               │
│  Browser / Streamlit UI                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Chat UI  │ │Dashboard │ │Doc Upload│ │Route Cmp │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                          │
│                   FastAPI Application                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │/chat     │ │/upload   │ │/shipments│ │/estimate │          │
│  │/query    │ │/parse    │ │/tracking │ │/routes   │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  AI ORCHESTRATION│ │  RAG PIPELINE   │ │  DATA LAYER     │
│                 │ │                 │ │                 │
│ Agent Router    │ │ Document Parser │ │ SQLite/Postgres  │
│ ┌─────────────┐ │ │ Chunker        │ │ (shipment data) │
│ │ Chat Agent  │ │ │ Embedder       │ │                 │
│ │ Duty Agent  │ │ │ ChromaDB       │ │ ChromaDB        │
│ │ Route Agent │ │ │ Retriever      │ │ (vector store)  │
│ │ Doc Agent   │ │ │ Reranker       │ │                 │
│ └─────────────┘ │ └─────────────────┘ │ JSON Files      │
│                 │                     │ (mock data)     │
│ LLM: Claude API │                     │                 │
│ or Gemini API   │                     └─────────────────┘
└─────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │ Claude/Gemini│ │ MarineTraffic│ │ FBR Duty DB  │           │
│  │ API (LLM)    │ │ (Free tier)  │ │ (scraped/CSV)│           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## Backend Architecture (FastAPI)

```
Request → FastAPI Router
              │
              ├─ /chat/query
              │      → QueryParser → AgentRouter → [ChatAgent]
              │                                      → RAGRetriever
              │                                      → ContextInjector
              │                                      → LLM (Claude)
              │                                      → ResponseFormatter
              │
              ├─ /documents/upload
              │      → FileParser → TextExtractor → Chunker
              │                                    → Embedder
              │                                    → ChromaDB.store()
              │
              ├─ /shipments/
              │      → ShipmentService → SQLite → MockDataLayer
              │
              ├─ /estimate/duty
              │      → DutyAgent → HSCodeLookup → RateCalculator
              │
              └─ /routes/compare
                     → RouteAgent → DataLookup → LLMReasoning
```

## Data Flow — AI Chat Query

```
User Types: "What duties will I pay for my Samsung phone shipment?"
                    │
                    ▼
            [QueryParser]
            Extracts: intent=duty_query, item=Samsung phone
                    │
                    ▼
            [AgentRouter]
            Routes to: DutyAgent + RAGRetriever
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
    [RAGRetriever]      [DutyAgent]
    Query ChromaDB      Lookup HS code
    for relevant        5-digit: 8517.13
    uploaded docs             │
          │                   ▼
          │            [RateCalculator]
          │            CD: 20%, RD: 0%
          │            ACD: 7%, ST: 18%
          │                   │
          └─────────┬─────────┘
                    ▼
            [ContextInjector]
            Builds prompt with:
            - Retrieved doc chunks
            - Duty rates
            - Shipment data
                    │
                    ▼
              [Claude API]
            Generates grounded answer
                    │
                    ▼
         [ResponseFormatter]
         Adds citations, confidence
                    │
                    ▼
              User sees answer
```

---

# SECTION 4 — MULTI-AGENT ARCHITECTURE

## Should You Even Use Multi-Agent in 7 Hours?

**Short Answer: Yes, but use a SIMPLIFIED orchestrator, not LangGraph.**

Here is why:

| Approach | Build Time | Demo Quality | Complexity |
|---|---|---|---|
| Single LLM with big prompt | 30 min | Medium | Low |
| Simple agent router (recommended) | 1.5 hrs | High | Medium |
| LangGraph multi-agent | 4+ hrs | Very High | Very High |
| CrewAI | 3+ hrs | High | High |

**Recommendation: Build a simple Python function-based router that selects the right "agent mode" based on intent classification. Each "agent" is a function with its own system prompt, tools, and context builder.**

## Agent Design (Simplified for Hackathon)

### Architecture: Intent Router Pattern

```python
class AgentRouter:
    def route(self, query: str, context: dict) -> AgentResponse:
        intent = self.classify_intent(query)  # LLM call or keyword match
        
        if intent == "shipment_tracking":
            return ShipmentAgent().run(query, context)
        elif intent == "duty_calculation":
            return DutyAgent().run(query, context)
        elif intent == "route_recommendation":
            return RouteAgent().run(query, context)
        elif intent == "document_question":
            return DocumentAgent().run(query, context)
        else:
            return GeneralChatAgent().run(query, context)
```

## Agent 1: Shipment Tracking Agent

**Role:** Retrieves and explains shipment status, ETA, delays

**Inputs:**
- User query (natural language)
- Shipment ID (extracted or provided)
- Shipment database records

**Outputs:**
- Current status with plain-English explanation
- ETA estimate
- Delay reason analysis
- Next steps

**System Prompt:**
```
You are a shipment tracking specialist for Pakistani importers. 
You have access to shipment data and must:
1. Report current status accurately
2. Explain delays in plain, practical language
3. Give realistic ETA based on available data
4. Flag any customs holds or issues
5. NEVER fabricate tracking data — only use provided data
6. If data is unavailable, say so clearly

Current shipment data: {shipment_json}
User query: {query}
```

**Tools:** `get_shipment_by_id()`, `get_delay_reasons()`, `calculate_eta()`

**Mock Data Strategy:** Pre-built JSON with 5 realistic shipments at different stages

---

## Agent 2: Customs & Duty Agent

**Role:** Calculates duty estimates, explains customs requirements

**Inputs:**
- Product description or HS code
- Country of origin
- Declared value (USD)
- Uploaded invoice (if any)

**Outputs:**
- Duty breakdown (CD, RD, ACD, ST, WHT)
- Total landed cost estimate
- Customs risk assessment
- Required documents list

**System Prompt:**
```
You are a Pakistani customs expert with deep knowledge of FBR regulations.
You MUST:
1. Calculate duties using the exact formula: 
   - Customs Duty (CD): [rate]% of CIF value
   - Regulatory Duty (RD): [rate]% if applicable  
   - Additional Customs Duty (ACD): 7% on dutiable value
   - Sales Tax: 18% on dutiable value + CD + RD + ACD
   - Withholding Tax: 5.5% for filers, 8% for non-filers
2. Show the FULL calculation breakdown
3. Cite the HS code and SRO if known
4. Flag any regulatory issues

Product: {product}
Origin: {origin}  
CIF Value (USD): {value}
Exchange Rate: {pkr_rate} PKR/USD
HS Code Data: {hs_data}
```

**Tools:** `lookup_hs_code()`, `get_duty_rates()`, `calculate_duties()`, `get_required_docs()`

**Dataset:** CSV of HS codes with duty rates (scraped from FBR/customs tariff)

---

## Agent 3: Route Recommendation Agent

**Role:** Compares shipping routes and provides recommendations

**Inputs:**
- Origin city/port
- Product type and weight
- Budget vs speed preference
- Urgency

**Outputs:**
- Top 2–3 route options with pros/cons
- Cost comparison table
- ETA comparison
- Recommendation with reasoning

**System Prompt:**
```
You are a freight routing expert specializing in Pakistan import corridors.
Compare shipping options and explain tradeoffs clearly.

Available routes data: {routes_data}
User preference (cost vs speed): {preference}
Origin: {origin}, Destination: {destination}
Product: {product}, Weight: {weight}

Provide:
1. Option A: [Route name] - Cost: $X, ETA: Y days
   Pros: ...
   Cons: ...
   
2. Option B: [Route name] - Cost: $X, ETA: Y days  
   Pros: ...
   Cons: ...

3. RECOMMENDATION: Option [X] because [specific reasoning]

Base recommendations ONLY on the provided data. Do not fabricate costs.
```

**Tools:** `get_route_data()`, `compare_freight_modes()`, `estimate_transit_time()`

---

## Agent 4: Document Intelligence Agent

**Role:** Answers questions about uploaded documents

**Inputs:**
- User query
- Retrieved document chunks (from ChromaDB)
- Document metadata

**Outputs:**
- Direct answer with source citation
- Missing information flags
- Document completeness check
- Anomaly detection

**System Prompt:**
```
You are a logistics document expert for Pakistani importers.
You have been given excerpts from the user's uploaded documents.

STRICT RULES:
1. ONLY answer from the provided document excerpts
2. If information is not in the documents, say "This information is not in your uploaded documents"
3. Always cite which document your answer comes from
4. Flag any discrepancies between documents (e.g., invoice value vs BOL value)
5. Check for missing required fields

Document excerpts:
{retrieved_chunks}

User question: {query}
```

**Tools:** `rag_retrieve()`, `check_document_completeness()`, `detect_anomalies()`

---

## Agent 5: General Chat / Routing Agent

**Role:** Handles general queries, routes to specialists

**Inputs:** Raw user query

**Outputs:** Either direct answer or routes to specialized agent

This is the "dispatcher" — a lightweight intent classifier that decides which agent handles the query.

```python
INTENT_KEYWORDS = {
    "tracking": ["where", "status", "arrived", "location", "tracking", "ETA", "delayed"],
    "duty": ["duty", "tax", "customs", "duties", "fee", "tariff", "charge", "HS code"],
    "route": ["route", "sea", "air", "shipping", "freight", "cheaper", "faster", "compare"],
    "document": ["invoice", "bill of lading", "BOL", "document", "PDF", "uploaded"],
}

def classify_intent(query: str) -> str:
    query_lower = query.lower()
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        scores[intent] = sum(1 for kw in keywords if kw in query_lower)
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
```

This is fast, free, and reliable. You don't need an LLM call just for routing.

---

# SECTION 5 — RAG PIPELINE

## Overview

```
INGESTION PIPELINE:
User Uploads PDF/Image
        │
        ▼
[File Type Detector]
        │
    ┌───┴───┐
    ▼       ▼
[PDF     [Image
Parser]  OCR]
    │       │
    └───┬───┘
        ▼
[Text Cleaner]
Remove headers/footers, fix encoding
        │
        ▼
[Semantic Chunker]
Split into meaningful chunks
        │
        ▼
[Metadata Extractor]
doc_type, date, shipment_id, etc.
        │
        ▼
[Embedder]
sentence-transformers/all-MiniLM-L6-v2
        │
        ▼
[ChromaDB]
Store embedding + chunk + metadata
        │
        ▼
"Document processed ✓"

RETRIEVAL PIPELINE:
User Query
        │
        ▼
[Query Embedder] (same model)/the embedder model
        │
        ▼
[ChromaDB Similarity Search]
Top-K=5 most similar chunks
        │
        ▼
[Metadata Filter]
Filter by user_id, doc_type if needed
        │
        ▼
[Reranker] (optional - cross-encoder)
Reorder by relevance
        │
        ▼
[Context Builder]
Assemble chunks into prompt context
        │
        ▼
[LLM with context]
        │
        ▼
[Grounded Response]
```

## Document Parsing Strategy

### PDF Parsing

```python
# Use PyMuPDF (fitz) — fastest, most reliable
import fitz

def parse_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# If PyMuPDF fails (scanned PDF), fall back to OCR:
# Use pytesseract or easyocr
import easyocr
reader = easyocr.Reader(['en'])
result = reader.readtext(image_path)
```

### Supported Document Types

| Document Type | Parser | Notes |
|---|---|---|
| Commercial Invoice (PDF) | PyMuPDF | Usually text-based |
| Bill of Lading (PDF) | PyMuPDF | May have tables |
| Customs Declaration | PyMuPDF + Table extractor | Complex structure |
| Packing List | PyMuPDF | Usually clean |
| Scanned images | EasyOCR | Slower, less accurate |
| HS Code PDFs | PyMuPDF | Large docs — filter pages |

## Chunking Strategy

**Recommended: Hybrid chunking — sentence-aware + size-bounded**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,        # Characters per chunk
    chunk_overlap=64,      # Overlap for continuity
    separators=["\n\n", "\n", ". ", " ", ""],  # Try these in order
    length_function=len
)

chunks = splitter.split_text(document_text)
```

**Why 512 characters?**
- Logistics documents have dense tabular data — too large chunks include irrelevant rows
- Too small chunks lose context (e.g., splitting an invoice line item)
- 512 chars ≈ 100–120 tokens — fits well in context without bloating

**Why overlap?**
- BOL clauses often span paragraphs
- 64-char overlap ensures clause boundaries aren't missed

## Embedding Models

| Model | Size | Speed | Quality | Cost | Recommendation |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 | 80MB | Very Fast | Good | Free | ✅ USE THIS |
| all-mpnet-base-v2 | 420MB | Medium | Better | Free | Use if time allows |
| text-embedding-3-small | Cloud | Fast | Excellent | $0.02/1M tokens | Fallback paid option |
| nomic-embed-text | 274MB | Fast | Very Good | Free | Good alternative |

**For hackathon: `sentence-transformers/all-MiniLM-L6-v2`**
- Loads in seconds
- No API key needed
- Good enough for logistics document retrieval
- 384-dimensional embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text: str) -> list[float]:
    return model.encode(text).tolist()
```

## ChromaDB Schema Design

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="shipment_documents",
    metadata={"hnsw:space": "cosine"}
)

# Store a chunk
collection.add(
    ids=[f"{doc_id}_{chunk_idx}"],
    embeddings=[embedding_vector],
    documents=[chunk_text],
    metadatas=[{
        "doc_id": "doc_001",
        "doc_type": "bill_of_lading",  # invoice, bol, customs, policy
        "filename": "BOL_2024_001.pdf",
        "shipment_id": "SHP_001",
        "user_id": "user_001",
        "upload_date": "2024-01-15",
        "page_number": 2,
        "chunk_index": 3,
    }]
)

# Retrieve
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={"user_id": "user_001"},  # Filter by user
    include=["documents", "metadatas", "distances"]
)
```

## Retrieval Strategy

### Step 1: Semantic Search
```python
def retrieve_chunks(query: str, user_id: str, n_results: int = 5):
    query_embedding = embed_text(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"user_id": user_id},
    )
    
    chunks = []
    for i, doc in enumerate(results['documents'][0]):
        chunks.append({
            "text": doc,
            "metadata": results['metadatas'][0][i],
            "distance": results['distances'][0][i]
        })
    
    return chunks
```

### Step 2: Context Assembly
```python
def build_rag_context(chunks: list) -> str:
    context = "RETRIEVED DOCUMENT EXCERPTS:\n\n"
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1}: {chunk['metadata']['filename']}, "
        context += f"Type: {chunk['metadata']['doc_type']}]\n"
        context += chunk['text']
        context += "\n\n---\n\n"
    return context
```

### Hallucination Prevention

1. **Grounding instruction in every prompt:** "Only answer from provided excerpts. If not found, say 'Not in uploaded documents.'"
2. **Source citation requirement:** Force the model to cite [Source N] in every factual claim
3. **Confidence thresholds:** If all retrieved distances > 0.7, warn user "Low confidence — documents may not contain this information"
4. **No-context fallback:** If no relevant chunks found, switch to knowledge-base-only mode with explicit disclaimer

---

# SECTION 6 — APIs & DATA SOURCES

## Complete Data Source Map

### 1. Shipment Tracking

| Source | Free? | What You Get | Hackathon Strategy |
|---|---|---|---|
| MarineTraffic Free | ✅ Yes (limited) | Vessel position, port info | Use free endpoints |
| Searates.com | ✅ Free tier | Container tracking | Register for API key |
| AfterShip | ✅ Free tier (50 tracks) | Multi-carrier tracking | Use for demo |
| VesselFinder | ✅ Web scraping | AIS vessel data | Scrape for demo |
| **MOCK DATA** | ✅ Best option | 100% reliable | Build this first |

**Recommended Hackathon Strategy:** Build a JSON mock dataset with 5–6 realistic shipments at different stages. Use MarineTraffic free endpoints for vessel visualization if time allows. Show the API integration architecture even if using mocks.

```json
// mock_shipments.json
[
  {
    "id": "SHP_2024_001",
    "status": "IN_TRANSIT",
    "origin": "Shenzhen, China",
    "destination": "Karachi, Pakistan",
    "port_of_loading": "CNSZX",
    "port_of_discharge": "PKKAR",
    "vessel": "COSCO HARMONY",
    "voyage_number": "VOY-2024-089",
    "container": "COSCO123456",
    "eta": "2024-02-15",
    "ata": null,
    "timeline": [
      {"event": "Booking Confirmed", "date": "2024-01-10", "status": "done"},
      {"event": "Cargo Loaded", "date": "2024-01-14", "status": "done"},
      {"event": "Departed Shenzhen", "date": "2024-01-15", "status": "done"},
      {"event": "Transshipment - Singapore", "date": "2024-01-20", "status": "done"},
      {"event": "In Transit", "date": "2024-01-22", "status": "current"},
      {"event": "Arrival Karachi", "date": "2024-02-15", "status": "pending"},
      {"event": "Customs Clearance", "date": "2024-02-16", "status": "pending"}
    ],
    "delay_days": 2,
    "delay_reason": "Port congestion in Singapore",
    "customs_status": "PENDING",
    "declared_value_usd": 15000,
    "hs_code": "8517.13",
    "product": "Mobile Phones",
    "importer": "Ahmed Electronics",
    "freight_type": "FCL",
    "container_size": "20FT"
  }
]
```

### 2. Customs & Duty Data

| Source | Free? | What You Get | How to Use |
|---|---|---|---|
| FBR Customs Tariff | ✅ Free (PDF) | Full HS code duty rates | Download & parse into CSV |
| Pakistan Customs website | ✅ Free | SRO notifications | Scrape or manual |
| WCO HS codes | ✅ Free | HS classification | Download database |
| PRAL online | ✅ Free | Duty calculator reference | Reference for validation |

**Build a CSV lookup table from FBR data:**

```csv
hs_code,description,cd_rate,rd_rate,acd_rate,st_rate,wht_filer,wht_nonfiler,notes
8517.13,"Smartphones",20,0,7,18,5.5,8,"Mobile phones incl. smartphones"
8471.30,"Laptops/Notebooks",0,0,0,18,5.5,8,"Duty-free laptops"
6109.10,"T-Shirts (Cotton)",20,15,7,18,5.5,8,"Textile item"
8703.23,"Cars 1000-1800cc",50,25,7,18,5.5,8,"Passenger vehicles"
...
```

**Duty Calculation Formula (Pakistan):**
```python
def calculate_duties(cif_value_usd: float, exchange_rate: float, 
                     cd_rate: float, rd_rate: float, 
                     acd_rate: float, is_filer: bool) -> dict:
    
    cif_pkr = cif_value_usd * exchange_rate
    
    cd = cif_pkr * (cd_rate / 100)
    rd = cif_pkr * (rd_rate / 100)
    acd = (cif_pkr + cd + rd) * (acd_rate / 100)
    
    dutiable_value = cif_pkr + cd + rd + acd
    sales_tax = dutiable_value * 0.18
    
    wht_rate = 0.055 if is_filer else 0.08
    wht = (cif_pkr + cd + rd) * wht_rate
    
    total_duties = cd + rd + acd + sales_tax + wht
    landed_cost = cif_pkr + total_duties
    
    return {
        "cif_pkr": round(cif_pkr, 2),
        "customs_duty": round(cd, 2),
        "regulatory_duty": round(rd, 2),
        "additional_customs_duty": round(acd, 2),
        "sales_tax": round(sales_tax, 2),
        "withholding_tax": round(wht, 2),
        "total_duties": round(total_duties, 2),
        "total_landed_cost": round(landed_cost, 2),
        "duty_as_percent_of_cif": round((total_duties / cif_pkr) * 100, 1)
    }
```

### 3. Route & Freight Data

| Route | Sea Days | Air Days | Sea Cost/kg | Air Cost/kg |
|---|---|---|---|---|
| Shenzhen → Karachi | 18–22 | 3–5 | $0.8–1.2 | $3.5–5.0 |
| Dubai → Karachi | 5–7 | 1–2 | $1.2–2.0 | $2.5–4.0 |
| New York → Karachi | 25–30 | 5–7 | $1.5–2.5 | $5.0–8.0 |
| Hamburg → Karachi | 20–25 | 4–6 | $1.3–2.0 | $4.5–7.0 |
| Tokyo → Karachi | 20–24 | 4–6 | $1.0–1.5 | $4.0–6.0 |

Store this as a static JSON lookup. The AI reasons over it.

### 4. Exchange Rate

```python
# Free API — no key needed
import requests

def get_pkr_rate():
    response = requests.get("https://open.er-api.com/v6/latest/USD")
    data = response.json()
    return data['rates']['PKR']

# Fallback — hardcode current rate
PKR_RATE_FALLBACK = 279.0  # Update at hackathon time
```

### 5. Port Congestion Data (Mock)

```python
PORT_CONGESTION = {
    "CNSZX": {"congestion": "LOW", "wait_days": 1},
    "SGSIN": {"congestion": "MEDIUM", "wait_days": 2},
    "AEJEA": {"congestion": "LOW", "wait_days": 1},
    "PKKAR": {"congestion": "HIGH", "wait_days": 5, "note": "Frequent delays at Karachi Port"},
    "PKPQQ": {"congestion": "MEDIUM", "wait_days": 3, "note": "Port Qasim - better than Karachi"},
}
```

---

# SECTION 7 — DATABASE DESIGN

## Recommended Stack

| Layer | Technology | Why |
|---|---|---|
| Relational | SQLite (dev) / PostgreSQL (prod) | Shipment records, user data |
| Vector | ChromaDB | Document embeddings |
| Cache | Python dict / Redis | Session cache |
| File storage | Local filesystem / S3 | Uploaded documents |

## SQLite Schema

```sql
-- Shipments table
CREATE TABLE shipments (
    id TEXT PRIMARY KEY,
    user_id TEXT DEFAULT 'demo_user',
    status TEXT,  -- BOOKED, LOADED, IN_TRANSIT, AT_PORT, CUSTOMS, DELIVERED, DELAYED
    origin_city TEXT,
    origin_country TEXT,
    destination_city TEXT,
    destination_port TEXT,
    vessel_name TEXT,
    voyage_number TEXT,
    container_number TEXT,
    eta DATE,
    ata DATE,
    delay_days INTEGER DEFAULT 0,
    delay_reason TEXT,
    customs_status TEXT,  -- PENDING, UNDER_REVIEW, CLEARED, HELD
    declared_value_usd REAL,
    hs_code TEXT,
    product_description TEXT,
    freight_type TEXT,  -- FCL, LCL, AIR
    container_size TEXT,
    carrier TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shipment timeline events
CREATE TABLE shipment_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shipment_id TEXT REFERENCES shipments(id),
    event_name TEXT,
    event_date DATE,
    location TEXT,
    status TEXT,  -- done, current, pending
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Uploaded documents
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    user_id TEXT DEFAULT 'demo_user',
    shipment_id TEXT REFERENCES shipments(id),
    filename TEXT,
    doc_type TEXT,  -- invoice, bill_of_lading, customs, packing_list, policy, hs_codes
    file_path TEXT,
    parsed_text TEXT,
    chunk_count INTEGER,
    embedding_status TEXT,  -- pending, processing, complete, error
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Duty calculations history
CREATE TABLE duty_calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT DEFAULT 'demo_user',
    shipment_id TEXT,
    hs_code TEXT,
    product_description TEXT,
    cif_value_usd REAL,
    exchange_rate REAL,
    customs_duty REAL,
    regulatory_duty REAL,
    additional_customs_duty REAL,
    sales_tax REAL,
    withholding_tax REAL,
    total_duties REAL,
    total_landed_cost REAL,
    is_filer BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat history
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,  -- user, assistant
    content TEXT,
    intent TEXT,
    agent_used TEXT,
    rag_sources TEXT,  -- JSON array of chunk IDs used
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HS Code lookup table
CREATE TABLE hs_codes (
    code TEXT PRIMARY KEY,
    description TEXT,
    cd_rate REAL,
    rd_rate REAL DEFAULT 0,
    acd_rate REAL DEFAULT 7,
    st_rate REAL DEFAULT 18,
    wht_filer REAL DEFAULT 5.5,
    wht_nonfiler REAL DEFAULT 8,
    notes TEXT,
    last_updated DATE
);
```

## ChromaDB Collections

```
Collection: "shipment_documents"
├── Purpose: User-uploaded document embeddings
├── Embedding: all-MiniLM-L6-v2 (384-dim)
└── Metadata fields: doc_id, doc_type, filename, shipment_id, user_id, chunk_index

Collection: "knowledge_base"
├── Purpose: Pre-loaded Pakistan customs/logistics knowledge
├── Embedding: all-MiniLM-L6-v2 (384-dim)  
└── Metadata fields: category, source, topic, last_updated
    Categories: customs_policy, duty_rates, port_info, shipping_guide, hs_classification
```

## Pre-loading Knowledge Base

Create a `knowledge_base/` folder with markdown files:

```
knowledge_base/
├── customs_procedures.md       # Customs clearance steps in Pakistan
├── required_documents.md       # Documents needed for import
├── duty_explanation.md         # How CD, RD, ACD, ST, WHT work
├── port_information.md         # Karachi Port, Port Qasim, Torkham
├── shipping_modes.md           # Air vs sea, FCL vs LCL
├── hs_code_guide.md            # How to find HS codes
├── common_delays.md            # Common delay reasons + solutions
├── freight_forwarder_guide.md  # How to choose forwarders
└── import_policy_2024.md       # Latest FBR import policy summary
```

Ingest these at startup so the AI has a knowledge base even without user uploads.

---

# SECTION 8 — BACKEND ARCHITECTURE

## Folder Structure

```
backend/
├── main.py                         # FastAPI app entry point
├── config.py                       # Settings, env vars, constants
├── requirements.txt
├── .env
│
├── api/                            # API Routes
│   ├── __init__.py
│   ├── chat.py                     # POST /chat/query
│   ├── documents.py                # POST /documents/upload, GET /documents
│   ├── shipments.py                # GET /shipments, GET /shipments/{id}
│   ├── duties.py                   # POST /duties/estimate
│   └── routes.py                   # POST /routes/compare
│
├── agents/                         # Agent definitions
│   ├── __init__.py
│   ├── router.py                   # AgentRouter - intent classification + routing
│   ├── chat_agent.py               # General chat agent
│   ├── shipment_agent.py           # Tracking + status agent
│   ├── duty_agent.py               # Customs + duty calculation agent
│   ├── route_agent.py              # Route comparison agent
│   └── document_agent.py           # Document Q&A agent
│
├── rag/                            # RAG Pipeline
│   ├── __init__.py
│   ├── parser.py                   # PDF + OCR parsing
│   ├── chunker.py                  # Text chunking
│   ├── embedder.py                 # Embedding generation
│   ├── vector_store.py             # ChromaDB operations
│   └── retriever.py                # Retrieval + context building
│
├── services/                       # Business logic
│   ├── __init__.py
│   ├── shipment_service.py         # Shipment CRUD + business logic
│   ├── duty_service.py             # Duty calculation logic
│   ├── document_service.py         # Document management
│   └── notification_service.py    # Alert generation
│
├── models/                         # Pydantic models + SQLite models
│   ├── __init__.py
│   ├── shipment.py
│   ├── document.py
│   ├── chat.py
│   └── duty.py
│
├── db/                             # Database
│   ├── __init__.py
│   ├── database.py                 # SQLite connection, session
│   ├── migrations.py               # Schema creation
│   └── seed_data.py                # Mock data seeding
│
├── data/                           # Static data files
│   ├── mock_shipments.json
│   ├── hs_codes.csv
│   ├── routes.json
│   ├── port_data.json
│   └── knowledge_base/             # Pre-loaded knowledge markdown files
│
└── utils/
    ├── __init__.py
    ├── llm_client.py               # Claude/Gemini API wrapper
    └── helpers.py                  # Utility functions
```

## Key Implementation Files

### main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import chat, documents, shipments, duties, routes
from db.database import init_db
from db.seed_data import seed_shipments
from rag.vector_store import init_knowledge_base

app = FastAPI(title="Pakistan Import Intelligence API", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], 
                   allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    init_db()
    seed_shipments()
    await init_knowledge_base()  # Load pre-built knowledge base

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(shipments.router, prefix="/api/shipments", tags=["Shipments"])
app.include_router(duties.router, prefix="/api/duties", tags=["Duties"])
app.include_router(routes.router, prefix="/api/routes", tags=["Routes"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Pakistan Import Intelligence"}
```

### config.py
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    LLM_PROVIDER: str = "anthropic"  # "anthropic" or "google"
    LLM_MODEL: str = "claude-sonnet-4-20250514"
    
    # Database
    DATABASE_URL: str = "sqlite:///./shipment_intel.db"
    CHROMA_PATH: str = "./chroma_db"
    
    # Embedding
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # App
    MAX_UPLOAD_SIZE_MB: int = 20
    PKR_EXCHANGE_RATE: float = 279.0  # Fallback rate
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### llm_client.py
```python
import anthropic
from config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def call_llm(system_prompt: str, user_message: str, 
              max_tokens: int = 1500) -> str:
    
    response = client.messages.create(
        model=settings.LLM_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text
```

### api/chat.py
```python
from fastapi import APIRouter
from pydantic import BaseModel
from agents.router import AgentRouter
from rag.retriever import retrieve_context

router = APIRouter()
agent_router = AgentRouter()

class ChatQuery(BaseModel):
    query: str
    session_id: str = "demo_session"
    shipment_id: str = None

@router.post("/query")
async def chat_query(request: ChatQuery):
    # 1. Retrieve relevant document context
    rag_context = retrieve_context(request.query, user_id="demo_user")
    
    # 2. Route to appropriate agent
    response = agent_router.route(
        query=request.query,
        rag_context=rag_context,
        shipment_id=request.shipment_id
    )
    
    return {
        "response": response.answer,
        "agent_used": response.agent_name,
        "sources": response.sources,
        "confidence": response.confidence
    }
```

### requirements.txt
```
fastapi==0.115.0
uvicorn==0.32.0
pydantic==2.9.0
pydantic-settings==2.5.0

# LLM
anthropic==0.39.0
google-generativeai==0.8.0

# RAG
sentence-transformers==3.3.0
chromadb==0.6.0
langchain-text-splitters==0.3.0

# Document parsing
pymupdf==1.24.14
easyocr==1.7.2
pillow==10.4.0

# Database
sqlalchemy==2.0.36

# Utilities
python-multipart==0.0.12
requests==2.32.0
pandas==2.2.0
python-dotenv==1.0.1
```

---

# SECTION 9 — FRONTEND ARCHITECTURE

## Technology Choice

### Streamlit vs Next.js for Hackathon

| Factor | Streamlit | Next.js |
|---|---|---|
| Setup time | 15 minutes | 45–90 minutes |
| Chart integration | Built-in | Needs libraries |
| File upload | Built-in | Custom component |
| Chat UI | `st.chat_*` | Custom |
| Looks professional | Medium | High |
| Learning curve | Minimal | Medium |
| Backend integration | Direct Python | REST API |
| **Hackathon verdict** | ✅ **USE THIS** | Too slow |

**Decision: Use Streamlit. You can make it look good with custom CSS. Ship faster.**

## Streamlit App Structure

```
frontend/
├── app.py                          # Main Streamlit entry point
├── pages/
│   ├── 1_Dashboard.py              # Shipment overview dashboard
│   ├── 2_Chat_Assistant.py         # AI chat interface
│   ├── 3_Document_Upload.py        # Upload & process documents
│   ├── 4_Duty_Calculator.py        # Customs duty estimator
│   └── 5_Route_Comparison.py       # Route & cost comparison
├── components/
│   ├── shipment_card.py            # Shipment card component
│   ├── timeline.py                 # Shipment timeline visualizer
│   └── chat_bubble.py              # Chat message component
├── utils/
│   └── api_client.py               # Backend API wrapper
└── assets/
    └── custom.css                  # Custom styling
```

## app.py (Main Entry)
```python
import streamlit as st

st.set_page_config(
    page_title="Pakistan Import Intelligence",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS injection
with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.title("Import Intelligence")
    st.markdown("---")
    st.markdown("**Powered by AI**")
    
    # Quick stats
    st.metric("Active Shipments", "6")
    st.metric("Pending Customs", "2")
    st.metric("Documents Indexed", "12")

st.title("🚢 Pakistan Import Intelligence Platform")
st.markdown("*Your AI-powered customs & logistics assistant*")
```

## pages/2_Chat_Assistant.py
```python
import streamlit as st
import requests

st.title("🤖 AI Shipment Assistant")
st.markdown("Ask anything about your shipments, customs, duties, or routes.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your AI import assistant. Ask me about:\n"
                   "• Shipment status & ETA\n"
                   "• Customs duties calculation\n"
                   "• Route recommendations\n"
                   "• Your uploaded documents"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📄 Sources"):
                for source in message["sources"]:
                    st.text(f"• {source}")

# Quick action buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📦 Track Shipment"):
        st.session_state.quick_query = "What is the status of my shipments?"
with col2:
    if st.button("💰 Estimate Duties"):
        st.session_state.quick_query = "Calculate duties for Samsung phones from China"
with col3:
    if st.button("🛣️ Compare Routes"):
        st.session_state.quick_query = "Should I use sea or air freight from Shenzhen?"
with col4:
    if st.button("📋 Check Documents"):
        st.session_state.quick_query = "What documents are missing for my shipment?"

# Chat input
if prompt := st.chat_input("Ask about your shipments...") or \
             st.session_state.get("quick_query"):
    
    if "quick_query" in st.session_state:
        prompt = st.session_state.quick_query
        del st.session_state.quick_query
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://localhost:8000/api/chat/query",
                json={"query": prompt, "session_id": "demo"}
            ).json()
        
        st.markdown(response["response"])
        
        if response.get("sources"):
            with st.expander("📄 Sources used"):
                for source in response["sources"]:
                    st.text(f"• {source}")
        
        st.caption(f"Agent: {response.get('agent_used', 'General')} | "
                  f"Confidence: {response.get('confidence', 'N/A')}")
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["response"],
        "sources": response.get("sources", [])
    })
```

## pages/1_Dashboard.py (Summary)
```python
import streamlit as st
import requests
import pandas as pd

st.title("📊 Shipment Dashboard")

# Summary metrics
shipments = requests.get("http://localhost:8000/api/shipments").json()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Shipments", len(shipments), delta="2 new")
with col2:
    in_transit = len([s for s in shipments if s['status'] == 'IN_TRANSIT'])
    st.metric("In Transit", in_transit)
with col3:
    delayed = len([s for s in shipments if s.get('delay_days', 0) > 0])
    st.metric("Delayed", delayed, delta=f"-{delayed} need attention", delta_color="inverse")
with col4:
    customs = len([s for s in shipments if s['customs_status'] == 'UNDER_REVIEW'])
    st.metric("Customs Review", customs)

st.markdown("---")

# Shipment cards
for shipment in shipments:
    status_color = {
        "IN_TRANSIT": "🟡", "DELIVERED": "🟢",
        "DELAYED": "🔴", "AT_PORT": "🟠", "BOOKED": "⚪"
    }.get(shipment['status'], "⚪")
    
    with st.expander(f"{status_color} {shipment['id']} — {shipment['product_description']} | ETA: {shipment['eta']}"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Origin:** {shipment['origin_city']}, {shipment['origin_country']}")
            st.write(f"**Vessel:** {shipment['vessel_name']}")
            st.write(f"**Container:** {shipment['container_number']}")
        with col2:
            st.write(f"**Status:** {shipment['status']}")
            st.write(f"**Customs:** {shipment['customs_status']}")
            if shipment.get('delay_days', 0) > 0:
                st.warning(f"⚠️ Delayed {shipment['delay_days']} days: {shipment['delay_reason']}")
```

---

# SECTION 10 — CLOUD & DEPLOYMENT

## Hackathon Deployment Stack

```
Recommended: LOCAL DEMO (No deployment needed for hackathon)
├── Backend:  uvicorn on localhost:8000
├── Frontend: streamlit on localhost:8501
└── DB:       SQLite file + ChromaDB folder

If you need to share/demo remotely:
├── Backend:  Render.com free tier (deploy FastAPI)
├── Frontend: Streamlit Cloud (free, instant)
└── DB:       Keep SQLite in repo for demo
```

**Why not deploy to cloud during hackathon?**
- Deployment takes 30–60 minutes you don't have
- Local demo is more reliable and faster
- You control the environment
- Screen-share works perfectly

## Docker Setup (Use AFTER hackathon for submission)

### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - LLM_PROVIDER=anthropic
    volumes:
      - ./backend/chroma_db:/app/chroma_db
      - ./backend/shipment_intel.db:/app/shipment_intel.db
      - ./backend/data:/app/data
    command: uvicorn main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
    command: streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps for OCR
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Post-Hackathon Deployment

| Service | Use Case | Cost |
|---|---|---|
| Google Cloud Run | FastAPI backend | Free tier generous |
| Railway.app | Full stack | $5/month |
| Render.com | FastAPI + Streamlit | Free tier |
| Streamlit Cloud | Frontend only | Free |
| Supabase | PostgreSQL | Free tier |
| Pinecone | Vector DB (prod) | Free tier |

---

# SECTION 11 — TEAM DIVISION

## Team of 3 — Optimal Split

```
MEMBER A: Backend + AI/RAG Lead
MEMBER B: Frontend + Integration Lead  
MEMBER C: Data + Content + QA Lead
```

## Member A — Backend & AI

**Hours 1–2:** Project setup + FastAPI skeleton + database + seed data
**Hours 3–4:** RAG pipeline (parser + embedder + ChromaDB)
**Hours 5–6:** Agent system (router + duty agent + chat agent)
**Hour 7:** Integration testing + bug fixes

**Owns:**
- All files in `backend/`
- LLM integration
- ChromaDB setup
- Duty calculation engine
- Agent prompts

---

## Member B — Frontend & Integration

**Hours 1–2:** Streamlit setup + page structure + custom CSS
**Hours 3–4:** Dashboard page + shipment cards + timeline
**Hours 5–6:** Chat UI + document upload page + duty calculator UI
**Hour 7:** Connect all pages to backend API + polish

**Owns:**
- All files in `frontend/`
- API client wrapper
- UI/UX polish
- Demo flow design
- Presentation slides

---

## Member C — Data, Content & QA

**Hours 1–2:** Build mock_shipments.json (10 realistic shipments) + hs_codes.csv
**Hours 3–4:** Write knowledge_base/ markdown files (8–10 files) + ingest them
**Hours 5–6:** Build routes.json + test all API endpoints + write demo script
**Hour 7:** Full demo run-through + fix issues + prepare pitch

**Owns:**
- `data/` folder content
- `knowledge_base/` markdown files
- HS code CSV (100+ codes)
- Mock shipment data
- End-to-end testing
- Demo presentation

---

## Dependency Map

```
Member C builds data    → Member A uses it for seeding
Member A builds API     → Member B consumes it in frontend
Member B builds UI      → Member C tests it
All three align at H4   → Integration checkpoint
```

## Communication Protocol
- Shared GitHub repo with simple branching: `main`, `backend`, `frontend`, `data`
- WhatsApp group for quick sync
- Sync at: H2, H4, H6 (brief 5-min standups)
- No long meetings — keep heads down

---

# SECTION 12 — 7-HOUR EXECUTION ROADMAP

## Critical Path

```
[H1] Foundation → [H2] Core Backend → [H3] RAG + AI → 
[H4] Integration Check → [H5] Frontend Polish → 
[H6] Full System Test → [H7] Demo Prep + Buffer
```

## Hour-by-Hour Plan

### HOUR 1 (0:00 – 1:00) — FOUNDATION
**All Members:**
- [ ] Create GitHub repo, share access
- [ ] Copy folder structure from this document
- [ ] Create `.env` with API keys
- [ ] Install all requirements

**Member A:**
- [ ] `main.py` + `config.py` + `requirements.txt`
- [ ] `db/database.py` (SQLite connection)
- [ ] `db/migrations.py` (create all tables)

**Member B:**
- [ ] `frontend/app.py` skeleton
- [ ] `frontend/pages/` empty files created
- [ ] `frontend/utils/api_client.py` stub

**Member C:**
- [ ] Create `mock_shipments.json` with 6 shipments (all stages)
- [ ] Create `hs_codes.csv` with 50+ codes from FBR tariff
- [ ] Create `routes.json` with 5 origin/destination pairs

**Exit Criteria:** All machines running with no import errors

---

### HOUR 2 (1:00 – 2:00) — CORE SERVICES
**Member A:**
- [ ] `db/seed_data.py` — load mock_shipments.json into SQLite
- [ ] `services/shipment_service.py` — CRUD operations
- [ ] `api/shipments.py` — GET /shipments, GET /shipments/{id}
- [ ] Test: `curl localhost:8000/api/shipments` returns data

**Member B:**
- [ ] `pages/1_Dashboard.py` — display shipment cards from API
- [ ] `pages/4_Duty_Calculator.py` — form UI (no logic yet)
- [ ] Connect to backend: `requests.get(BACKEND_URL + "/api/shipments")`

**Member C:**
- [ ] Write 6 knowledge_base markdown files
- [ ] Start `services/duty_service.py` (calculation formula)
- [ ] Test duty calculation formula independently

**Exit Criteria:** Dashboard shows shipment cards from database

---

### HOUR 3 (2:00 – 3:00) — RAG PIPELINE
**Member A:**
- [ ] `rag/parser.py` — PDF text extraction with PyMuPDF
- [ ] `rag/chunker.py` — RecursiveCharacterTextSplitter  
- [ ] `rag/embedder.py` — Load all-MiniLM-L6-v2
- [ ] `rag/vector_store.py` — ChromaDB init + add/query operations
- [ ] `rag/vector_store.py` — `init_knowledge_base()` function
- [ ] Test: knowledge base loads on startup

**Member B:**
- [ ] `pages/3_Document_Upload.py` — file uploader UI
- [ ] Show upload progress + success message
- [ ] `pages/2_Chat_Assistant.py` — basic chat UI (no AI yet)

**Member C:**
- [ ] Finish all 8 knowledge_base markdown files
- [ ] Build `api/duties.py` with duty calculation endpoint
- [ ] Test duty endpoint with curl

**Exit Criteria:** Upload a PDF → it gets parsed and chunked. Knowledge base loads at startup.

---

### HOUR 4 (3:00 – 4:00) — AI INTEGRATION [INTEGRATION CHECKPOINT]
**5-minute standup at 4:00 — verify integration is working**

**Member A:**
- [ ] `agents/router.py` — intent classifier (keyword-based)
- [ ] `agents/duty_agent.py` — duty calculation + explanation agent
- [ ] `agents/document_agent.py` — RAG-based document Q&A agent
- [ ] `agents/chat_agent.py` — general logistics Q&A
- [ ] `api/chat.py` — POST /chat/query endpoint
- [ ] `utils/llm_client.py` — Claude/Gemini API wrapper

**Member B:**
- [ ] Connect chat page to `/api/chat/query`
- [ ] Connect duty calculator page to `/api/duties/estimate`
- [ ] Show response in chat bubbles

**Member C:**
- [ ] Full end-to-end test: upload PDF → ask question about it
- [ ] Full end-to-end test: duty calculation
- [ ] Document all bugs found

**Exit Criteria:** Can upload a document and ask a question about it. Duty calculator returns a breakdown.

---

### HOUR 5 (4:00 – 5:00) — ROUTE COMPARISON + POLISH
**Member A:**
- [ ] `agents/route_agent.py` — route comparison with AI reasoning
- [ ] `api/routes.py` — POST /routes/compare
- [ ] Bug fixes from Hour 4 testing

**Member B:**
- [ ] `pages/5_Route_Comparison.py` — route comparison UI
- [ ] Dashboard analytics (simple charts with st.bar_chart)
- [ ] Custom CSS for professional look

**Member C:**
- [ ] Build `routes.json` with detailed route data
- [ ] Write demo script (exact sequence of actions for demo)
- [ ] Prepare 3–4 sample questions for each demo scenario

**Exit Criteria:** Route comparison works. Dashboard looks polished.

---

### HOUR 6 (5:00 – 6:00) — FULL SYSTEM INTEGRATION TEST
**All Members: Full dry run of the demo**

Run through this exact demo sequence:
1. Open dashboard → see shipment overview
2. Click on delayed shipment → see details
3. Go to Chat → ask "Why is SHP_001 delayed?"
4. Go to Documents → upload sample_invoice.pdf
5. Go to Chat → ask "What is the declared value in my invoice?"
6. Go to Duty Calculator → calculate duties for smartphones
7. Go to Route Comparison → compare sea vs air from Shenzhen

Fix anything that breaks. Log all issues. Member A fixes backend bugs. Member B fixes UI bugs.

---

### HOUR 7 (6:00 – 7:00) — DEMO POLISH + PRESENTATION
**Member A:** 
- Final bug fixes
- Make sure all API endpoints return fast (<3 seconds)
- Prepare backup: if API fails, have hardcoded response JSONs ready

**Member B:**
- Record a screen capture of the working demo
- Prepare presentation slides (5–7 slides)
- Polish UI final pass

**Member C:**
- Write pitch script
- Prepare demo questions and answers
- Test demo one more time on clean restart

---

# SECTION 13 — PROMPT ENGINEERING

## System Prompts

### Master System Prompt (All Agents)
```
You are an AI-powered import intelligence assistant specializing in Pakistani customs and logistics.

YOUR EXPERTISE:
- Pakistan customs regulations (FBR, PRAL, customs tariff)
- Import procedures at Karachi Port and Port Qasim
- Duty calculation: CD, RD, ACD, Sales Tax, WHT
- Freight forwarding and shipping routes
- Trade document interpretation (BOL, Invoice, Packing List, LC)
- HS code classification
- Common import delays and how to avoid them

YOUR CORE RULES:
1. NEVER fabricate shipment tracking data — only use data provided to you
2. ALWAYS show your calculation when estimating duties
3. ALWAYS cite your source when answering from documents: "[Source: filename]"
4. If you don't know something, say "I don't have that information" — don't guess
5. Be practical and actionable — Pakistani importers need real advice, not theory
6. Use clear, simple English that non-experts can understand

PAKISTAN CONTEXT:
- Currency: PKR (Pakistani Rupee), currently ~279 PKR/USD
- Tax authority: FBR (Federal Board of Revenue)
- Main ports: Karachi Port (KPT), Port Qasim
- Border crossings: Torkham (Afghanistan), Wagah (India), Chaman
- Import policy governed by: SRO notifications from Ministry of Commerce
```

### RAG Prompt Template
```python
RAG_PROMPT = """
CONTEXT FROM UPLOADED DOCUMENTS:
{rag_context}

SHIPMENT DATA:
{shipment_data}

USER QUESTION:
{query}

INSTRUCTIONS:
- Answer the question using ONLY the context provided above
- If the answer is in the documents, cite: [Source: document name]
- If the answer requires calculation, show the full calculation
- If the information is NOT in the provided context, say: 
  "This information is not available in your uploaded documents. 
   Based on general knowledge: [answer]"
- Keep the answer practical and concise
- Format tables when comparing multiple options

YOUR ANSWER:
"""
```

### Duty Calculation Prompt
```python
DUTY_PROMPT = """
Calculate Pakistan import duties for the following:

Product: {product}
HS Code: {hs_code}
Country of Origin: {origin}
CIF Value: USD {cif_value}
Current PKR/USD Rate: {pkr_rate}

Duty Rates (from FBR Customs Tariff):
- Customs Duty (CD): {cd_rate}%
- Regulatory Duty (RD): {rd_rate}%
- Additional Customs Duty (ACD): {acd_rate}%
- Sales Tax: 18%
- Withholding Tax: {wht_rate}% (filer status: {filer_status})

REQUIRED OUTPUT FORMAT:

**Duty Calculation for {product}**

| Component | Rate | Amount (PKR) |
|---|---|---|
| CIF Value | - | {cif_pkr} |
| Customs Duty | {cd_rate}% | {cd_amount} |
| Regulatory Duty | {rd_rate}% | {rd_amount} |
| Additional Customs Duty | {acd_rate}% | {acd_amount} |
| Sales Tax (18%) | 18% | {st_amount} |
| Withholding Tax | {wht_rate}% | {wht_amount} |
| **TOTAL DUTIES** | - | **{total_duties}** |
| **TOTAL LANDED COST** | - | **{landed_cost}** |

**Duty as % of CIF: {duty_percent}%**

**Key Notes:**
[Add any relevant notes about exemptions, SROs, or special conditions]

**Documents Required:**
[List required import documents]
"""
```

### Route Recommendation Prompt
```python
ROUTE_PROMPT = """
Compare shipping routes for a Pakistani importer.

Product: {product}
Weight: {weight} kg
From: {origin}
To: Pakistan ({destination_preference})
Budget Priority: {priority} (cost-saving / time-saving / balanced)

AVAILABLE ROUTE DATA:
{routes_json}

PORT CONGESTION STATUS:
{port_congestion}

Provide a structured comparison:

1. OPTION A: [Route Name]
   - Mode: Sea/Air
   - Transit Time: X days
   - Estimated Cost: $X–$Y (per kg or FCL/LCL)
   - Port: [Port name]
   - Customs Risk: Low/Medium/High
   - Pros: [2–3 specific advantages]
   - Cons: [2–3 specific disadvantages]

2. OPTION B: [Route Name]
   [same format]

3. MY RECOMMENDATION: Option [X]
   Because: [specific, data-driven reasoning based on their priorities]
   
   Hidden Costs to Consider:
   - [List 2–3 often-missed costs]
   
   Timing Advice:
   - [Seasonal or current market advice]

Base ALL recommendations on the provided route data.
Do not fabricate specific freight prices if not in the data.
"""
```

### Hallucination Prevention Protocol
```python
GROUNDING_CHECK_PROMPT = """
Review your response and check:
1. Did you cite a source for every specific fact? If not, add [General Knowledge] tag
2. Did you fabricate any tracking numbers, prices, or dates? Remove them
3. Is every calculation verifiable? Show the formula
4. Are any claims unverifiable from provided context? Flag them

If the user's question cannot be answered from available data, 
respond with:
"I don't have enough information to answer this precisely. 
Here's what I know: [general knowledge only]
To get the exact answer, I recommend: [specific action]"
"""
```

---

# SECTION 14 — DEMO STRATEGY

## The 5-Minute Demo Flow

### Scene 1: The Problem (30 seconds)
"Ahmed imports phones from Shenzhen. Right now he has 3 shipments, doesn't know where they are, doesn't know what duties he'll pay, and has a stack of PDFs he can't read. That's the problem we're solving."

**Screen:** Show blank WhatsApp conversation with freight forwarder (relatable pain)

### Scene 2: The Dashboard (45 seconds)
"Here's Ahmed's dashboard. One place for all his shipments."

**Screen:** Show dashboard with 6 shipment cards
- Point to delayed shipment: "This one's delayed 3 days — the system already flagged it"
- Show customs hold: "This one's in customs review — system explains why"

### Scene 3: AI Chat — The Wow Moment (90 seconds)
"Now watch this — Ahmed types in plain English."

**Type:** "Why is my shipment SHP_001 delayed?"
**Show:** AI responds with specific delay reason, port congestion data, new ETA

**Type:** "What documents are missing for my Samsung phone shipment?"
**Show:** AI checks uploaded documents and lists missing items with specific citations

### Scene 4: Document Upload (60 seconds)
"Ahmed uploads the invoice he just received."

**Action:** Upload `sample_invoice.pdf`
**Type:** "What is the declared value and HS code in my invoice?"
**Show:** AI extracts and cites exact values from the document

### Scene 5: Duty Calculator (45 seconds)
"No more surprise bills at the port."

**Action:** Enter Samsung phone, $15,000 CIF, China origin
**Show:** Full duty breakdown table — CD, ACD, ST, WHT, total PKR amount

### Scene 6: Route Comparison (30 seconds)
"Sea vs air — the AI explains the tradeoff with numbers."

**Action:** Enter route comparison
**Show:** Two options with costs, ETAs, recommendation

### Closing (30 seconds)
"This is what every Pakistani importer needs. We built this in 7 hours. With 3 months, we add live tracking APIs, Urdu support, customs agent integration, and bank financing links."

## Judge Psychology

| What Judges Want | How You Deliver It |
|---|---|
| Real problem, not solution looking for problem | Lead with Ahmed's story |
| Technical depth | Show RAG working — "it's reading HIS documents" |
| Business viability | $60B import market, 85% SME |
| Demo that works | Pre-test everything, have backup screenshots |
| Scalability story | 3-minute future roadmap at the end |

## Demo Dataset Preparation

Prepare these files BEFORE the hackathon:
1. `sample_invoice.pdf` — realistic commercial invoice (Samsung phones, Shenzhen, $15K)
2. `sample_bol.pdf` — Bill of Lading for the same shipment
3. `sample_customs.pdf` — Pakistan customs declaration form (GD form)
4. 6 mock shipments at different stages in the database

---

# SECTION 15 — FUTURE SCALABILITY

## 6-Month Startup Roadmap

| Phase | Timeline | What to Build | Revenue Model |
|---|---|---|---|
| MVP (Current) | 0–1 month | Core demo features | N/A |
| Beta | 1–3 months | Real API integrations, user auth | Waitlist |
| Launch | 3–6 months | 50 beta users, Karachi | Freemium |
| Growth | 6–12 months | Lahore + Faisalabad, mobile | SaaS $29–99/mo |
| Scale | 12–24 months | Enterprise, customs integration | Enterprise deals |

## Production Architecture (12 months)

```
Production Stack:
├── Backend: FastAPI on Google Cloud Run (auto-scaling)
├── Database: PostgreSQL on Cloud SQL (managed)
├── Vector DB: Pinecone (production-grade, managed)
├── LLM: Claude API with caching (Anthropic)
├── Queue: Cloud Pub/Sub (async document processing)
├── Storage: Google Cloud Storage (documents)
├── Auth: Firebase Auth (user management)
├── Frontend: Next.js on Vercel (SSR, fast)
├── Monitoring: Google Cloud Monitoring + Sentry
└── CDN: Cloudflare
```

## Real API Integrations (Paid)

| API | Cost | What It Adds |
|---|---|---|
| MarineTraffic API | $50/mo | Real vessel tracking |
| AfterShip | $19/mo | Multi-carrier container tracking |
| Freightos API | Custom | Real freight rates |
| World Bank Tariff API | Free | International duty rates |
| Pakistan Customs WEBOC | Integration | Official customs data |
| Open Exchange Rates | $12/mo | Live exchange rates |

## Revenue Streams

1. **SaaS Subscription:** Importers pay $29–99/month for the platform
2. **Per-Document Processing:** $0.10–$0.50 per document parsed
3. **Customs Agent Marketplace:** 10–15% commission on agent bookings
4. **Freight Comparison (Affiliate):** Revenue share with freight forwarders
5. **Enterprise:** $500–$2000/month for large importers + API access
6. **White-label:** License to customs clearing companies

## Agentic Workflow (Future)

```
Future: Automated Compliance Agent
User ships → AI reads BOL → 
  Auto-checks missing documents → 
  Auto-calculates duties → 
  Auto-files pre-arrival declaration → 
  Notifies importer of clearance status →
  Recommends customs agent if needed
```

---

# SECTION 16 — RISKS & FAILURE POINTS

## Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| LLM API goes down | Low | Critical | Have both Anthropic + Google keys; fallback prompt |
| ChromaDB init fails | Medium | High | Pre-test before hackathon, have backup SQLite search |
| PDF parsing fails | Medium | High | Use PyMuPDF + EasyOCR fallback; test 3 PDF types |
| Frontend can't connect to backend | Medium | High | Set CORS to *, test localhost connections early |
| LLM hallucination in demo | Medium | High | Use tight system prompts, pre-test all demo queries |
| No internet at venue | Low | Critical | Download all models, use offline fallback |
| Slow LLM response (>10 sec) | Medium | Medium | Add streaming, show typing indicator |
| Team member gets blocked | Medium | High | Cross-training on critical paths |

## Technical Risk Deep Dive

### Risk 1: Hallucination in Demo
**Problem:** AI confidently gives wrong duty rate during demo
**Mitigation:**
- Pre-test EVERY demo query 10+ times before demo
- Use very strict system prompt with "only use provided data" instruction
- For duty calculation, use hard-coded formula, not AI math
- Show sources in UI — judges see AI is grounded, not hallucinating

### Risk 2: ChromaDB Fails to Initialize
**Problem:** Embedding model fails to load, knowledge base empty
**Mitigation:**
```python
# Always have a fallback
try:
    context = chroma_retrieve(query)
except Exception as e:
    # Fallback to keyword search over raw markdown files
    context = keyword_search_knowledge_base(query)
    logger.warning(f"ChromaDB failed, using fallback: {e}")
```

### Risk 3: PDF Upload Fails
**Problem:** Judge uploads a complex PDF, parsing fails
**Mitigation:**
- Use pre-tested sample PDFs in demo (you control the documents)
- Have upload pre-loaded ("for demo speed, I've already loaded Ahmed's documents")
- Always have the `sample_invoice.pdf` you built tested and confirmed working

### Risk 4: API Key Exhausted
**Problem:** Hit rate limits on Claude API during demo
**Mitigation:**
- Use Claude with generous rate limits (Anthropic API)
- Cache responses for demo queries: if query matches pre-run query, return cached response
- Have Gemini as backup with same prompt format

```python
RESPONSE_CACHE = {}  # In-memory cache for demo

def cached_llm_call(prompt_hash: str, system: str, user: str) -> str:
    if prompt_hash in RESPONSE_CACHE:
        return RESPONSE_CACHE[prompt_hash]
    
    response = call_llm(system, user)
    RESPONSE_CACHE[prompt_hash] = response
    return response
```

### Risk 5: Slow Internet / No WiFi
**Problem:** API calls to Claude timeout or fail
**Mitigation:**
- Download `all-MiniLM-L6-v2` model before hackathon
- Pre-cache 10 key demo responses
- Have static "demo mode" that serves pre-computed answers
- SQLite runs offline, ChromaDB runs offline

```python
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# In agent:
if DEMO_MODE:
    return PRECOMPUTED_DEMO_RESPONSES.get(intent, fallback_response)
```

## Hackathon-Specific Risks

| Risk | Prevention |
|---|---|
| Feature scope creep | Stick to this document's MVP scope |
| Over-engineering | Ship simple, polish later |
| Git conflicts | Work in separate folders, merge at H4/H6 |
| Forgetting to push demo data | Commit mock data + ChromaDB to repo |
| Demo environment different from dev | Test on a fresh machine at H6 |
| LLM responses too slow for demo | Pre-cache, use streaming |

---

# APPENDIX: QUICK REFERENCE

## Environment Variables (.env)
```bash
# LLM
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514

# App
DATABASE_URL=sqlite:///./shipment_intel.db
CHROMA_PATH=./chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
PKR_EXCHANGE_RATE=279.0
DEMO_MODE=false
```

## Key Commands
```bash
# Setup
pip install -r requirements.txt
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Run backend
uvicorn main:app --reload --port 8000

# Run frontend
streamlit run app.py

# Seed database
python db/seed_data.py

# Test API
curl http://localhost:8000/api/shipments
curl -X POST http://localhost:8000/api/chat/query -H "Content-Type: application/json" -d '{"query": "Where is my shipment?"}'
```

## Pre-Hackathon Checklist
- [ ] Anthropic API key obtained and tested
- [ ] Google Gemini API key as backup
- [ ] Python 3.11 installed on all machines
- [ ] All packages from requirements.txt tested for installation
- [ ] `all-MiniLM-L6-v2` downloaded locally
- [ ] sample_invoice.pdf + sample_bol.pdf + sample_customs.pdf prepared
- [ ] GitHub repo created and shared
- [ ] Mock data files created
- [ ] FBR customs tariff CSV with 50+ HS codes ready
- [ ] Knowledge base markdown files written
- [ ] Demo script written and rehearsed
- [ ] Fallback plan for every critical component documented

---

*Document generated as a complete hackathon blueprint.*
*Build sequence: Data first → Backend → RAG → Agents → Frontend → Integration → Demo*
*Remember: A working demo with 5 features beats a broken demo with 10 features.*
