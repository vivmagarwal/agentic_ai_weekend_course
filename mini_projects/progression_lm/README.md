# Progression LM

A lightweight "notebook + chat" application that allows users to upload PDFs, ask questions, and receive answers clearly labeled as **From PDF** or **From Web** with comprehensive source attribution.

## Features

- 📚 Create notebooks from PDFs with chat interface
- 🔍 RAG-powered answers with PDF context awareness
- 🌐 Automatic web search fallback via Tavily
- 📝 Clear source attribution (PDF citations with page numbers OR web links)
- ⚡ Single-file backend (FastAPI) and frontend (React + Flowbite via CDN)

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Tavily API key ([Get one here](https://tavily.com))

### Installation

1. **Clone the repository and navigate to the project:**

```bash
cd mini_projects/001_progression_lm
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install backend dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

4. **Configure environment variables:**

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
CONFIDENCE_THRESHOLD=0.35
MAX_PDF_SOURCES=5
MAX_WEB_SOURCES=3
PORT=8000
CORS_ORIGINS=http://localhost:3000,file://
```

### Running the Application

1. **Start the server:**

```bash
cd backend
python app.py
# Or: uvicorn app:app --reload --port 8000
```

2. **Open the application:**

The backend serves the frontend automatically. Simply visit:

**http://localhost:8000**

That's it! Everything runs on a single port.

## API Documentation

### Health Check

**GET** `/api/v1/health`

Returns server status.

**Response:**
```json
{
  "status": "healthy"
}
```

### Upload PDF

**POST** `/api/v1/upload`

Upload a PDF to create a new notebook.

**Request:** (multipart/form-data)
- `name`: Notebook name (string, required)
- `pdf`: PDF file (file, required)

**Response:**
```json
{
  "success": true,
  "message": "Uploaded successfully",
  "session_id": "uuid-here",
  "filename": "document.pdf",
  "num_chunks": 42,
  "processing_time": 3.14
}
```

### Query Notebook

**POST** `/api/v1/query`

Ask a question about the uploaded PDF.

**Request:**
```json
{
  "session_id": "uuid-here",
  "question": "What is the main topic of this document?",
  "stream": false
}
```

**Response (PDF source):**
```json
{
  "success": true,
  "answer": "The document discusses...",
  "source": "pdf",
  "pdf_sources": [
    {
      "file_name": "document.pdf",
      "page_start": 3,
      "page_end": 5
    }
  ],
  "chunks_used": 5,
  "processing_time": 1.23,
  "metadata": {
    "model": "gpt-4o-mini",
    "tokens": 1234
  }
}
```

**Response (Web source):**
```json
{
  "success": true,
  "answer": "Based on web search...",
  "source": "web",
  "web_sources": [
    {
      "title": "Example Article",
      "url": "https://example.com",
      "snippet": "This article discusses..."
    }
  ],
  "processing_time": 2.45,
  "metadata": {
    "model": "gpt-4o-mini",
    "tokens": 987
  }
}
```

### List Notebooks

**GET** `/api/v1/notebooks`

Get all notebooks (sorted by creation date).

**Response:**
```json
{
  "success": true,
  "notebooks": [
    {
      "id": "uuid-here",
      "name": "My Notebook",
      "created_at": "2025-10-04T12:00:00Z",
      "sources_count": 1
    }
  ]
}
```

### Get PDF File

**GET** `/api/v1/notebooks/{id}/pdf/{file_name}`

Stream a PDF file for viewing.

**Response:** PDF file stream

## Example Queries

Here are some example questions you can ask after uploading a PDF:

- "What is the main topic of this document?"
- "Summarize the key findings in 3 bullet points"
- "What does page 5 say about [specific topic]?"
- "When was this written?" (will use web search if not in PDF)

## How It Works

1. **PDF Upload**: The system extracts text from PDFs using PyMuPDF4LLM, chunks it, and creates embeddings
2. **Vector Storage**: Embeddings are stored in FAISS for fast similarity search
3. **Query Processing**:
   - Retrieves top-k similar chunks from the PDF
   - Checks confidence threshold (mean cosine similarity ≥ 0.35)
   - If confident: Answers using PDF context with source attribution
   - If not confident: Falls back to Tavily web search
4. **Response**: Returns answer with clear source labels and clickable citations

## Architecture

### Backend (Single File: `backend/app.py`)

- FastAPI application with CORS middleware
- Pydantic models for request/response validation
- PDF processing with PyMuPDF4LLM (page-level chunking)
- FAISS vector store with persistence
- LangChain for RAG pipeline
- Tavily integration for web search fallback
- SQLite for notebook metadata

### Frontend (Single File: `frontend/index.html`)

- React 18 via CDN
- Flowbite components for UI
- Tailwind CSS for styling
- Fetch-based API client
- Client-side routing (home/chat views)

### Data Storage

```
backend/data/
├── pdfs/{session_id}/          # Uploaded PDF files
├── index/{session_id}/         # FAISS vector indices
└── db.sqlite                   # Notebook metadata
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for embeddings and LLM
- `TAVILY_API_KEY`: Tavily API key for web search
- `CONFIDENCE_THRESHOLD`: PDF confidence threshold (default: 0.35)
- `MAX_PDF_SOURCES`: Max PDF sources in response (default: 5)
- `MAX_WEB_SOURCES`: Max web sources in response (default: 3)
- `PORT`: Server port (default: 8000)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

### Tuning the Confidence Threshold

The `CONFIDENCE_THRESHOLD` determines when to use PDF vs web search:

- **Lower values (0.2-0.3)**: More likely to use PDF, fewer web searches
- **Higher values (0.4-0.5)**: More likely to use web search, stricter PDF matching
- **Default (0.35)**: Balanced between PDF precision and web recall

## Troubleshooting

### PDF Upload Fails

- **Check file size**: Ensure PDF is not corrupted or too large
- **Check format**: Only PDF files are supported
- **Check API keys**: Verify OpenAI API key is valid

### Web Search Not Working

- **Check Tavily API key**: Verify key is valid and has credits
- **Check internet connection**: Ensure server can access Tavily API
- **Check error logs**: See backend console for detailed errors

### No Answer from PDF

- **Lower confidence threshold**: Try reducing `CONFIDENCE_THRESHOLD` to 0.25-0.30
- **Check PDF quality**: Ensure PDF has extractable text (not just images)
- **Rephrase question**: Try asking in different ways

### CORS Errors

- **Update CORS_ORIGINS**: Add your frontend origin to `.env`
- **Check protocol**: Ensure using correct protocol (http:// vs file://)

## Performance

- **PDF Ingestion**: ~15 seconds for 10-page PDF on laptop CPU
- **Query Response**:
  - First token: ≤ 3 seconds
  - Full answer: ≤ 8 seconds (typical)
- **Memory**: < 2 GB steady-state

## Roadmap

### v1.0 (Current)
- ✅ Single PDF per notebook
- ✅ Source attribution: "From PDF" with page ranges OR "From Web" with links
- ✅ Local-only deployment
- ✅ Single-file backend and frontend

### v1.1 (Planned)
- Multiple PDFs per notebook
- Mixed answers: source="mixed" with both PDF and web sources
- Improved UI with PDF viewer

### v1.2 (Future)
- PDF highlighting (jump to specific page/section)
- Chat history persistence
- Export chat transcripts

### v1.3 (Future)
- Basic authentication
- Cloud storage option (S3/GCS)
- Multi-user support

## License

This project is part of the Agentic AI Course.

## Contributing

This is a learning project. Feel free to experiment and extend functionality!

## Support

For issues and questions, please refer to the engineering plan document: `progression-lm-engineering-plan.md`
