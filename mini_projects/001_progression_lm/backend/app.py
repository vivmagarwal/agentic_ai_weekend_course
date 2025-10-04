"""
Progression LM - Single-file FastAPI Backend
A RAG-powered notebook chat application with PDF and web search capabilities.
"""

import os
import uuid
import time
import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

import pymupdf4llm

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.35"))
MAX_PDF_SOURCES = int(os.getenv("MAX_PDF_SOURCES", "5"))
MAX_WEB_SOURCES = int(os.getenv("MAX_WEB_SOURCES", "3"))
PORT = int(os.getenv("PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,file://").split(",")

# Paths
DATA_DIR = Path("data")
PDFS_DIR = DATA_DIR / "pdfs"
INDEX_DIR = DATA_DIR / "index"
DB_PATH = DATA_DIR / "db.sqlite"
FRONTEND_DIR = Path("../frontend")
FRONTEND_HTML = FRONTEND_DIR / "index.html"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
PDFS_DIR.mkdir(exist_ok=True)
INDEX_DIR.mkdir(exist_ok=True)

# Initialize models
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tavily_search = TavilySearch(max_results=MAX_WEB_SOURCES, topic="general")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Pydantic Models
class PdfSource(BaseModel):
    file_name: str
    page_start: Optional[int] = None
    page_end: Optional[int] = None

class WebSource(BaseModel):
    title: str
    url: str
    snippet: str

class QueryRequest(BaseModel):
    session_id: str
    question: str
    stream: bool = False

class QueryResponse(BaseModel):
    success: bool = True
    answer: str
    source: str  # 'pdf', 'web', or 'mixed'
    pdf_sources: Optional[List[PdfSource]] = None
    web_sources: Optional[List[WebSource]] = None
    chunks_used: Optional[int] = None
    processing_time: float
    metadata: Dict[str, Any] = {}

class UploadResponse(BaseModel):
    success: bool = True
    message: str = "Uploaded successfully"
    session_id: str
    filename: str
    num_chunks: int
    processing_time: float

class Notebook(BaseModel):
    id: str
    name: str
    created_at: str
    sources_count: int

# Database setup
def init_db():
    """Initialize SQLite database for notebook metadata"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notebooks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            sources_count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Database operations
def insert_notebook(notebook_id: str, name: str):
    """Insert a new notebook record"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notebooks (id, name, created_at, sources_count) VALUES (?, ?, ?, ?)",
        (notebook_id, name, datetime.utcnow().isoformat(), 1)
    )
    conn.commit()
    conn.close()

def get_all_notebooks() -> List[Notebook]:
    """Get all notebooks sorted by creation date"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, created_at, sources_count FROM notebooks ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [Notebook(id=r[0], name=r[1], created_at=r[2], sources_count=r[3]) for r in rows]

# FastAPI app
app = FastAPI(title="Progression LM API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": str(exc),
            "error_code": "INTERNAL_ERROR"
        }
    )

# PDF Processing Functions
def process_pdf(file_path: str, session_id: str) -> tuple[FAISS, int]:
    """
    Process PDF using PyMuPDF4LLM with page-level chunking.
    Returns FAISS vectorstore and number of chunks.
    """
    # Load PDF with page-level chunks
    md_text = pymupdf4llm.to_markdown(file_path, page_chunks=True)

    # Parse the markdown output to create documents with metadata
    documents = []
    current_page = 1

    # Split by page markers if present
    if isinstance(md_text, list):
        # PyMuPDF4LLM returns list of dicts with page_chunks=True
        for item in md_text:
            page_num = item.get('metadata', {}).get('page', current_page)
            text = item.get('text', '')

            doc = Document(
                page_content=text,
                metadata={
                    'file_name': os.path.basename(file_path),
                    'page_number': page_num,
                    'page_start': page_num,
                    'page_end': page_num,
                    'session_id': session_id
                }
            )
            documents.append(doc)
            current_page = page_num + 1
    else:
        # Fallback: single document
        doc = Document(
            page_content=md_text,
            metadata={
                'file_name': os.path.basename(file_path),
                'page_number': 1,
                'page_start': 1,
                'page_end': 1,
                'session_id': session_id
            }
        )
        documents.append(doc)

    # Split documents while preserving metadata
    chunks = text_splitter.split_documents(documents)

    # Create FAISS vectorstore
    vectorstore = FAISS.from_documents(chunks, embedding_model)

    # Save index
    index_path = INDEX_DIR / session_id
    index_path.mkdir(exist_ok=True)
    vectorstore.save_local(str(index_path))

    return vectorstore, len(chunks)

def load_vectorstore(session_id: str) -> FAISS:
    """Load existing FAISS vectorstore"""
    index_path = INDEX_DIR / session_id
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Notebook not found")

    return FAISS.load_local(
        str(index_path),
        embedding_model,
        allow_dangerous_deserialization=True
    )

def build_pdf_sources(chunks: List[Document]) -> List[PdfSource]:
    """Build PDF sources list from retrieved chunks"""
    sources_dict = {}

    for chunk in chunks:
        metadata = chunk.metadata
        file_name = metadata.get('file_name', 'unknown.pdf')
        page_start = metadata.get('page_start', metadata.get('page_number', 1))
        page_end = metadata.get('page_end', metadata.get('page_number', 1))

        key = f"{file_name}:{page_start}-{page_end}"
        if key not in sources_dict:
            sources_dict[key] = PdfSource(
                file_name=file_name,
                page_start=page_start,
                page_end=page_end
            )

    # Return up to MAX_PDF_SOURCES
    return list(sources_dict.values())[:MAX_PDF_SOURCES]

def perform_web_search(question: str) -> List[WebSource]:
    """Perform web search using Tavily"""
    try:
        results = tavily_search.invoke({"query": question})

        # Normalize results to WebSource format
        web_sources = []

        # Tavily returns dict with 'results' key containing the list
        if isinstance(results, dict):
            results_list = results.get('results', [])
        elif isinstance(results, list):
            results_list = results
        else:
            results_list = []

        for result in results_list[:MAX_WEB_SOURCES]:
            if isinstance(result, dict):
                web_sources.append(WebSource(
                    title=result.get('title', 'Untitled'),
                    url=result.get('url', ''),
                    snippet=result.get('content', result.get('snippet', ''))
                ))

        return web_sources
    except Exception as e:
        print(f"Web search error: {e}")
        import traceback
        traceback.print_exc()
        return []

def check_answer_in_context(question: str, context: str) -> bool:
    """Use LLM to check if the context contains information to answer the question"""
    check_prompt = ChatPromptTemplate.from_template("""
You are evaluating whether the provided context contains sufficient information to answer the user's question.

Context:
{context}

Question: {question}

Does the context contain enough information to answer this question?
Respond with ONLY "YES" if the context provides a clear answer, or "NO" if it does not.

Response:""")

    chain = check_prompt | llm | StrOutputParser()
    response = chain.invoke({"context": context, "question": question}).strip().upper()

    return "YES" in response

# LLM Prompts
answer_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant helping a user understand information from their documents.

Context from PDF:
{context}

User Question: {question}

Provide a clear, accurate answer based on the context above. Be concise but comprehensive.

Answer:
""")

web_answer_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant helping a user with their question using web search results.

User Question: {question}

Web Search Results:
{web_context}

Provide a clear, accurate answer based on the web search results above. Cite sources where appropriate.

Answer:
""")

# API Endpoints

# Serve Frontend
@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file"""
    if FRONTEND_HTML.exists():
        return FileResponse(str(FRONTEND_HTML))
    raise HTTPException(status_code=404, detail="Frontend not found")

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/v1/upload", response_model=UploadResponse)
async def upload_pdf(
    name: str = Form(...),
    pdf: UploadFile = File(...)
):
    """Upload a PDF and create a notebook"""
    start_time = time.time()

    # Validate file type
    if not pdf.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Generate session ID
    session_id = str(uuid.uuid4())

    # Create session directory
    session_pdf_dir = PDFS_DIR / session_id
    session_pdf_dir.mkdir(exist_ok=True)

    # Save PDF
    pdf_path = session_pdf_dir / pdf.filename
    with open(pdf_path, "wb") as f:
        content = await pdf.read()
        f.write(content)

    # Process PDF
    try:
        vectorstore, num_chunks = process_pdf(str(pdf_path), session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF processing failed: {str(e)}")

    # Save to database
    insert_notebook(session_id, name)

    processing_time = time.time() - start_time

    return UploadResponse(
        session_id=session_id,
        filename=pdf.filename,
        num_chunks=num_chunks,
        processing_time=processing_time
    )

@app.post("/api/v1/query", response_model=QueryResponse)
async def query_notebook(request: QueryRequest):
    """Query a notebook with RAG + web fallback"""
    start_time = time.time()

    # Load vectorstore
    try:
        vectorstore = load_vectorstore(request.session_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load notebook: {str(e)}")

    # Retrieve top-k chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    chunks = retriever.invoke(request.question)

    # Build context from chunks
    context = "\n\n".join([chunk.page_content for chunk in chunks]) if chunks else ""

    # Check if context can answer the question using LLM
    can_answer_from_pdf = False
    if context.strip():
        can_answer_from_pdf = check_answer_in_context(request.question, context)

    # Decision: PDF vs Web
    if can_answer_from_pdf:
        # Answer from PDF
        chain = answer_prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": request.question})

        pdf_sources = build_pdf_sources(chunks)

        processing_time = time.time() - start_time

        return QueryResponse(
            answer=answer,
            source="pdf",
            pdf_sources=pdf_sources,
            web_sources=None,
            chunks_used=len(chunks),
            processing_time=processing_time,
            metadata={"model": "gpt-4o-mini", "can_answer": True}
        )
    else:
        # Fallback to web search
        web_sources = perform_web_search(request.question)

        if not web_sources:
            raise HTTPException(
                status_code=404,
                detail="No information found in PDF and web search failed"
            )

        web_context = "\n\n".join([
            f"Title: {src.title}\nURL: {src.url}\nContent: {src.snippet}"
            for src in web_sources
        ])

        chain = web_answer_prompt | llm | StrOutputParser()
        answer = chain.invoke({"question": request.question, "web_context": web_context})

        processing_time = time.time() - start_time

        return QueryResponse(
            answer=answer,
            source="web",
            pdf_sources=None,
            web_sources=web_sources,
            chunks_used=None,
            processing_time=processing_time,
            metadata={"model": "gpt-4o-mini", "can_answer": False}
        )

@app.get("/api/v1/notebooks")
async def list_notebooks():
    """List all notebooks"""
    notebooks = get_all_notebooks()
    return {"success": True, "notebooks": [nb.dict() for nb in notebooks]}

@app.delete("/api/v1/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: str):
    """Delete a notebook and all associated data"""
    import shutil

    # Delete from database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notebooks WHERE id = ?", (notebook_id,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notebook not found")

    # Delete PDF files
    pdf_dir = PDFS_DIR / notebook_id
    if pdf_dir.exists():
        shutil.rmtree(pdf_dir)

    # Delete FAISS index
    index_dir = INDEX_DIR / notebook_id
    if index_dir.exists():
        shutil.rmtree(index_dir)

    return {"success": True, "message": "Notebook deleted successfully"}

@app.get("/api/v1/notebooks/{notebook_id}/pdf/{file_name}")
async def get_pdf(notebook_id: str, file_name: str):
    """Serve PDF file"""
    # Path sanitization
    file_name = os.path.basename(file_name)
    pdf_path = PDFS_DIR / notebook_id / file_name

    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")

    def iter_file():
        with open(pdf_path, "rb") as f:
            yield from f

    return StreamingResponse(
        iter_file(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename={file_name}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
