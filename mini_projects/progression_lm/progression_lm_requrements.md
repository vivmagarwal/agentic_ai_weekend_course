# Progression LM — Product Requirements Document

**A lightweight RAG-powered notebook application where users upload PDFs, ask questions, and receive answers with clear source attribution—either "From PDF" with page citations or "From Web" with clickable links.**

---

## Table of Contents

1. [Overview](#1-overview)
2. [Goals & Non-Goals](#2-goals--non-goals)
3. [User Stories](#3-user-stories)
4. [User Experience & UI Flow](#4-user-experience--ui-flow)
5. [Source Attribution System](#5-source-attribution-system)
6. [Technical Architecture](#6-technical-architecture)
7. [API Specification](#7-api-specification)
8. [Implementation Guide](#8-implementation-guide)
9. [Performance & Quality](#9-performance--quality)
10. [Acceptance Criteria](#10-acceptance-criteria)

---

## 1. Overview

**Progression LM** is a single-page RAG (Retrieval-Augmented Generation) application that combines PDF-based knowledge retrieval with web search fallback. Users create notebooks by uploading PDFs, then interact with an AI assistant that:

- **Answers from PDFs** when information is available in uploaded documents
- **Falls back to web search** (Tavily) when PDF content is insufficient
- **Clearly attributes sources** with visual badges and clickable citations

**Key differentiators:**
- Zero-build architecture (single-file backend + single-file frontend)
- Transparent source attribution with both PDF and web citations
- LLM-based semantic relevance checking for accurate source selection

---

## 2. Goals & Non-Goals

### ✅ Goals

1. **Notebook Management**: Create, view, and delete PDF-based notebooks
2. **Intelligent Chat**: Chat interface with RAG-powered responses
3. **Source Transparency**: Always show whether answers come from PDF or web
4. **Citation Quality**:
   - PDF sources: File name + page numbers
   - Web sources: Title + URL + snippet
5. **Simple Architecture**: Single-file FastAPI backend + single-file React frontend
6. **Single Port**: Everything served from `http://localhost:8000`

### ❌ Non-Goals (v1)

- Multi-user authentication or sharing
- File types beyond PDF
- In-PDF annotations or highlighting
- Streaming responses
- Mobile-optimized UI
- Cloud deployment (local-first)

---

## 3. User Stories

### US-1: Notebook Management
**As a user**, I want to create notebooks from PDFs so I can organize my documents and ask questions about them.

**Acceptance:**
- ✅ See all my notebooks on the home screen
- ✅ Create new notebook with name + PDF upload
- ✅ Delete unwanted notebooks
- ✅ See notebook metadata (creation date, source count)

### US-2: PDF-Based Chat
**As a user**, I want to ask questions about my PDFs and receive accurate answers with page citations.

**Acceptance:**
- ✅ Open any notebook and start chatting
- ✅ See "From PDF" badge when answer comes from my documents
- ✅ See PDF sources with file names and page numbers
- ✅ Click PDF sources to open the document

### US-3: Web Fallback
**As a user**, when my question isn't answered by PDFs, I want the system to search the web automatically.

**Acceptance:**
- ✅ System detects when PDF doesn't have relevant information
- ✅ Automatically performs web search (Tavily)
- ✅ Shows "From Web" badge for web-sourced answers
- ✅ Displays web sources with titles, URLs, and snippets
- ✅ Web links open in new tab

### US-4: Markdown Support
**As a user**, I want AI responses formatted with proper markdown for better readability.

**Acceptance:**
- ✅ Headers, bold, italic render correctly
- ✅ Lists (ordered/unordered) are formatted
- ✅ Code blocks have syntax highlighting
- ✅ Links are clickable

---

## 4. User Experience & UI Flow

### 4.1 Home Page (Notebook Grid)

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  Progression LM              [+ Create Notebook]│
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐  ┌──────────────┐             │
│  │      +       │  │  TOK Guide   │  [🗑️ hover] │
│  │              │  │  10/4/2025   │             │
│  │ Create new   │  │ • 1 source(s)│             │
│  │  notebook    │  └──────────────┘             │
│  └──────────────┘                                │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Elements:**
- **Header**: "Progression LM" title, "Create Notebook" button (top-right)
- **Grid**:
  - Dashed placeholder card with "+" icon and "Create new notebook" text
  - Notebook cards showing:
    - Notebook name (bold)
    - Creation date
    - Source count (e.g., "• 1 source(s)")
  - Delete button (trash icon) appears on hover in top-right of each card

**Interactions:**
- Click notebook card → Open chat view
- Click "+ Create Notebook" → Open modal
- Hover notebook card → Show delete button
- Click delete → Confirm → Remove notebook

### 4.2 Create Notebook Modal

**Layout:**
```
┌─────────────────────────────────┐
│  Create New Notebook            │
├─────────────────────────────────┤
│  Notebook Name                  │
│  ┌─────────────────────────┐   │
│  │                         │   │
│  └─────────────────────────┘   │
│                                 │
│  PDF File                       │
│  ┌──────────┐ No file chosen   │
│  │Choose File│                  │
│  └──────────┘                   │
│                                 │
│  [Cancel]        [Create]       │
└─────────────────────────────────┘
```

**Validation:**
- Name: Required, non-empty
- PDF: Required, must be `.pdf` file
- Create button disabled until both valid

**Behavior:**
- On success: Modal closes, new card appears in grid
- On error: Show error message in modal
- Cancel: Close modal without changes

### 4.3 Chat Interface

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  ← TOK Guide                                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  Start a conversation                           │
│  Ask questions about your PDF                   │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ what are 12 core TOK Concepts        [user]│
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │ The 12 core Theory of Knowledge concepts│  │
│  │ are:                                     │  │
│  │ • Evidence                               │  │
│  │ • Certainty                              │  │
│  │ • Truth                                  │  │
│  │ ...                                      │  │
│  │                                          │  │
│  │ [From PDF]                               │  │
│  │                                          │  │
│  │ PDF Sources:                             │  │
│  │ 📄 ToK guide.pdf (pages 12)             │  │
│  │ 📄 ToK guide.pdf (pages 11)             │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
├─────────────────────────────────────────────────┤
│  Ask a question...                     [Send]   │
│  Press Enter to send                            │
└─────────────────────────────────────────────────┘
```

**Message Types:**

1. **User Messages**
   - Blue bubble, right-aligned
   - Plain text display

2. **Assistant Messages (From PDF)**
   - White bubble with border, left-aligned
   - Markdown-rendered content
   - Green "From PDF" badge
   - PDF Sources section:
     - "PDF Sources:" header
     - List of sources: `📄 filename (pages X-Y)`
     - Clickable to open PDF

3. **Assistant Messages (From Web)**
   - White bubble with border, left-aligned
   - Markdown-rendered content
   - Blue "From Web" badge
   - Web Sources section:
     - "Web Sources:" header
     - List with:
       - 🔗 Title (bold, clickable link)
       - URL (shown in snippet)
       - Snippet preview (gray text)
     - Links open in new tab

**Markdown Rendering:**
- Headers (H1, H2, H3) with proper sizing
- **Bold** and *italic* text
- Ordered and unordered lists
- Code blocks with dark background
- Inline `code` with gray background
- Blockquotes with left border
- Clickable links

---

## 5. Source Attribution System

### 5.1 Architecture Overview

```
User Question
     ↓
Retrieve top-5 chunks from FAISS
     ↓
Check if context can answer question (LLM)
     ↓
   YES ────────────────────────→ NO
     ↓                            ↓
Answer from PDF              Tavily Web Search
     ↓                            ↓
Build pdf_sources           Build web_sources
     ↓                            ↓
source="pdf"                 source="web"
```

### 5.2 PDF Source Attribution

**Backend Flow:**
1. PyMuPDF4LLM extracts PDF with page-level chunks
2. Each chunk stored with metadata:
   ```python
   {
       'file_name': 'ToK guide.pdf',
       'page_number': 12,
       'page_start': 12,
       'page_end': 12,
       'session_id': 'uuid'
   }
   ```
3. On retrieval, gather chunks and extract unique sources:
   ```python
   def build_pdf_sources(chunks: List[Document]) -> List[PdfSource]:
       sources_dict = {}
       for chunk in chunks:
           metadata = chunk.metadata
           file_name = metadata.get('file_name', 'unknown.pdf')
           page_start = metadata.get('page_start', 1)
           page_end = metadata.get('page_end', 1)

           key = f"{file_name}:{page_start}-{page_end}"
           if key not in sources_dict:
               sources_dict[key] = PdfSource(
                   file_name=file_name,
                   page_start=page_start,
                   page_end=page_end
               )

       return list(sources_dict.values())[:MAX_PDF_SOURCES]
   ```

**Frontend Rendering:**
```jsx
{message.pdfSources?.map((src, idx) => (
    <a
        href={`/api/v1/notebooks/${notebookId}/pdf/${src.file_name}`}
        target="_blank"
    >
        📄 {src.file_name}
        {src.page_start && ` (pages ${src.page_start}${
            src.page_end !== src.page_start ? `-${src.page_end}` : ''
        })`}
    </a>
))}
```

### 5.3 Web Source Attribution

**Backend Flow:**
1. Tavily search returns dict:
   ```python
   {
       'query': '...',
       'results': [
           {'title': '...', 'url': '...', 'content': '...', 'score': 0.88},
           ...
       ]
   }
   ```
2. Normalize to WebSource format:
   ```python
   def perform_web_search(question: str) -> List[WebSource]:
       results = tavily_search.invoke({"query": question})

       # Handle dict with 'results' key
       if isinstance(results, dict):
           results_list = results.get('results', [])
       elif isinstance(results, list):
           results_list = results
       else:
           results_list = []

       web_sources = []
       for result in results_list[:MAX_WEB_SOURCES]:
           web_sources.append(WebSource(
               title=result.get('title', 'Untitled'),
               url=result.get('url', ''),
               snippet=result.get('content', result.get('snippet', ''))
           ))

       return web_sources
   ```

**Frontend Rendering:**
```jsx
{message.webSources?.map((src, idx) => (
    <a href={src.url} target="_blank" rel="noopener noreferrer">
        <span>🔗</span>
        <div>
            <div className="font-medium">{src.title}</div>
            <div className="text-gray-600 text-xs">{src.snippet}</div>
        </div>
    </a>
))}
```

### 5.4 Relevance Detection (Critical Logic)

**Problem:** FAISS always returns chunks, even if irrelevant. Simple text-length heuristics fail.

**Solution:** LLM-based semantic relevance checking:

```python
def check_answer_in_context(question: str, context: str) -> bool:
    """Use LLM to check if context contains sufficient information"""
    check_prompt = ChatPromptTemplate.from_template("""
You are evaluating whether the provided context contains sufficient information to answer the user's question.

Context:
{context}

Question: {question}

Does the context contain enough information to answer this question?
Respond with ONLY "YES" if the context provides a clear answer, or "NO" if it does not.

Response:""")

    chain = check_prompt | llm | StrOutputParser()
    response = chain.invoke({
        "context": context,
        "question": question
    }).strip().upper()

    return "YES" in response
```

**Query Flow:**
```python
# 1. Retrieve chunks
chunks = retriever.invoke(question)
context = "\n\n".join([chunk.page_content for chunk in chunks])

# 2. Check relevance with LLM
can_answer_from_pdf = False
if context.strip():
    can_answer_from_pdf = check_answer_in_context(question, context)

# 3. Route based on relevance
if can_answer_from_pdf:
    # Answer from PDF with pdf_sources
    return QueryResponse(source="pdf", pdf_sources=build_pdf_sources(chunks), ...)
else:
    # Fallback to web with web_sources
    web_sources = perform_web_search(question)
    return QueryResponse(source="web", web_sources=web_sources, ...)
```

---

## 6. Technical Architecture

### 6.1 Backend (Single-File FastAPI)

**File:** `backend/app.py`

**Stack:**
- **Framework**: FastAPI with Uvicorn
- **PDF Processing**: PyMuPDF4LLM (page-level chunking)
- **Embeddings**: OpenAI `text-embedding-3-large`
- **Vector Store**: FAISS (CPU-friendly, local persistence)
- **LLM**: OpenAI `gpt-4o-mini`
- **Web Search**: Tavily (via `langchain-tavily`)
- **Database**: SQLite (notebook metadata)
- **Text Splitting**: LangChain `RecursiveCharacterTextSplitter`

**Directory Structure:**
```
backend/
├── app.py              # Single-file FastAPI app
├── requirements.txt
├── .env
└── data/
    ├── pdfs/{session_id}/
    ├── index/{session_id}/
    └── db.sqlite
```

**Key Components:**

1. **Configuration** (lines 30-40)
   ```python
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
   CONFIDENCE_THRESHOLD = 0.35  # Unused (legacy)
   MAX_PDF_SOURCES = 5
   MAX_WEB_SOURCES = 3
   PORT = 8000
   ```

2. **Models** (lines 56-59)
   ```python
   embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
   llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
   tavily_search = TavilySearch(max_results=3)
   text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
   ```

3. **PDF Processing** (lines 165-221)
   - Extract with PyMuPDF4LLM (page chunks)
   - Create Documents with metadata
   - Split into smaller chunks (preserving metadata)
   - Embed and store in FAISS
   - Save index to disk

4. **Query Logic** (lines 382-454)
   - Load FAISS index
   - Retrieve top-5 chunks
   - Check relevance with LLM
   - Route to PDF or web
   - Build appropriate sources
   - Return QueryResponse

5. **Delete Logic** (lines 472-498)
   - Delete from SQLite
   - Remove PDF files (shutil.rmtree)
   - Remove FAISS index
   - Return success

### 6.2 Frontend (Single-File React)

**File:** `frontend/index.html`

**Stack:**
- **Framework**: React 18 (via CDN)
- **Styling**: Tailwind CSS (CDN) + Flowbite (CDN)
- **Markdown**: Marked.js (CDN)
- **Transpiler**: Babel Standalone (for JSX in browser)

**Key Components:**

1. **API Service** (lines 34-98)
   ```javascript
   const api = {
       async uploadNotebook(name, pdfFile) { /* FormData */ },
       async queryPDF(sessionId, question) { /* POST /query */ },
       async getNotebooks() { /* GET /notebooks */ },
       async deleteNotebook(notebookId) { /* DELETE /notebooks/{id} */ },
       getPDFUrl(notebookId, fileName) { /* Build URL */ }
   }
   ```

2. **Message Component** (lines 101-198)
   - User messages: Blue bubble, right-aligned
   - Assistant messages: White bubble with:
     - Markdown rendering (`marked.parse`)
     - Badge (green "From PDF" / blue "From Web")
     - PDF sources (with page numbers, clickable)
     - Web sources (with title, URL, snippet)

3. **Home Component** (lines 398-510)
   - Fetch notebooks on mount
   - Render grid with cards
   - Handle create/delete
   - Refresh on changes

4. **Chat Component** (lines 182-328)
   - Message list with auto-scroll
   - Input form with Enter-to-send
   - Loading states
   - Error handling

5. **App Component** (lines 512-564)
   - View routing (home ↔ chat)
   - Modal state management
   - Pass props to children

**Markdown Styles** (lines 24-39)
```css
.markdown-content h1 { font-size: 1.875rem; font-weight: 700; ... }
.markdown-content h2 { font-size: 1.5rem; font-weight: 600; ... }
.markdown-content code { background: #f3f4f6; font-family: monospace; ... }
.markdown-content pre { background: #1f2937; color: #f9fafb; ... }
```

### 6.3 Data Flow

**Upload Flow:**
```
User selects PDF → FormData → POST /api/v1/upload
                                      ↓
                            Save to pdfs/{session_id}/
                                      ↓
                            Extract with PyMuPDF4LLM
                                      ↓
                            Chunk + Embed → FAISS
                                      ↓
                            Save index to index/{session_id}/
                                      ↓
                            Insert to SQLite
                                      ↓
                            Return {session_id, num_chunks, ...}
```

**Query Flow:**
```
User types question → POST /api/v1/query {session_id, question}
                                ↓
                      Load FAISS index
                                ↓
                      Retrieve top-5 chunks
                                ↓
                      Build context string
                                ↓
                      LLM: Can answer? (YES/NO)
                                ↓
                        YES             NO
                         ↓               ↓
                    Answer from PDF   Tavily search
                         ↓               ↓
                    pdf_sources      web_sources
                         ↓               ↓
                    Return QueryResponse
                                ↓
                      Frontend renders message with badge + sources
```

**Delete Flow:**
```
User clicks delete → Confirm → DELETE /api/v1/notebooks/{id}
                                         ↓
                               DELETE FROM notebooks WHERE id=?
                                         ↓
                               shutil.rmtree(pdfs/{id}/)
                                         ↓
                               shutil.rmtree(index/{id}/)
                                         ↓
                               Return {success: true}
                                         ↓
                               Frontend refreshes notebook list
```

---

## 7. API Specification

### 7.1 Upload Notebook

**Endpoint:** `POST /api/v1/upload`

**Content-Type:** `multipart/form-data`

**Request:**
```
name: "TOK Guide"
pdf: <binary PDF file>
```

**Response:** `200 OK`
```json
{
    "success": true,
    "message": "Uploaded successfully",
    "session_id": "e2c70f9c-bdf0-4326-967f-56d728add9d5",
    "filename": "ToK guide.pdf",
    "num_chunks": 58,
    "processing_time": 12.34
}
```

**Errors:**
- `400`: Not a PDF file
- `500`: PDF processing failed

### 7.2 Query Notebook

**Endpoint:** `POST /api/v1/query`

**Request:**
```json
{
    "session_id": "e2c70f9c-bdf0-4326-967f-56d728add9d5",
    "question": "What are the 12 TOK concepts?",
    "stream": false
}
```

**Response (PDF Source):** `200 OK`
```json
{
    "success": true,
    "answer": "The 12 core Theory of Knowledge (TOK) concepts are:\n\n1. Evidence\n2. Certainty\n3. Truth\n...",
    "source": "pdf",
    "pdf_sources": [
        {
            "file_name": "ToK guide.pdf",
            "page_start": 12,
            "page_end": 12
        },
        {
            "file_name": "ToK guide.pdf",
            "page_start": 11,
            "page_end": 11
        }
    ],
    "web_sources": null,
    "chunks_used": 5,
    "processing_time": 3.45,
    "metadata": {
        "model": "gpt-4o-mini",
        "can_answer": true
    }
}
```

**Response (Web Source):** `200 OK`
```json
{
    "success": true,
    "answer": "The founders of Axelerant Technologies are Ankur Gupta and Abhi Goel. Ankur Gupta currently serves as the CEO...",
    "source": "web",
    "pdf_sources": null,
    "web_sources": [
        {
            "title": "Axelerant - 2025 Company Profile, Team & Competitors - Tracxn",
            "url": "https://tracxn.com/d/companies/axelerant/__ZO9FbyT...",
            "snippet": "The founders of Axelerant are Ankur Gupta and Abhi Goel. Ankur Gupta is the CEO of Axelerant..."
        },
        {
            "title": "Axelerant - Crunchbase Company Profile & Funding",
            "url": "https://www.crunchbase.com/organization/axelerant",
            "snippet": "Legal Name Axelerant Technologies, Inc. ; Company Type For Profit ; Founders Abhi Goel, Ankur Gupta."
        }
    ],
    "chunks_used": null,
    "processing_time": 7.08,
    "metadata": {
        "model": "gpt-4o-mini",
        "can_answer": false
    }
}
```

**Errors:**
- `404`: Notebook not found
- `404`: No information found (PDF + web both failed)
- `500`: Query processing failed

### 7.3 List Notebooks

**Endpoint:** `GET /api/v1/notebooks`

**Response:** `200 OK`
```json
{
    "success": true,
    "notebooks": [
        {
            "id": "e2c70f9c-bdf0-4326-967f-56d728add9d5",
            "name": "TOK Guide",
            "created_at": "2025-10-04T08:34:19.053102",
            "sources_count": 1
        }
    ]
}
```

### 7.4 Delete Notebook

**Endpoint:** `DELETE /api/v1/notebooks/{notebook_id}`

**Response:** `200 OK`
```json
{
    "success": true,
    "message": "Notebook deleted successfully"
}
```

**Errors:**
- `404`: Notebook not found

### 7.5 Get PDF File

**Endpoint:** `GET /api/v1/notebooks/{notebook_id}/pdf/{file_name}`

**Response:** `200 OK`
```
Content-Type: application/pdf
Content-Disposition: inline; filename=ToK guide.pdf

<binary PDF stream>
```

**Errors:**
- `404`: PDF not found

### 7.6 Health Check

**Endpoint:** `GET /api/v1/health`

**Response:** `200 OK`
```json
{
    "status": "healthy"
}
```

### 7.7 Serve Frontend

**Endpoint:** `GET /`

**Response:** `200 OK`
```
Content-Type: text/html

<HTML content from frontend/index.html>
```

---

## 8. Implementation Guide

### 8.1 Backend Setup

**1. Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**2. Configure Environment**
```bash
cp .env.example .env
# Edit .env:
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

**3. Run Server**
```bash
python app.py
# Server starts on http://localhost:8000
```

### 8.2 Key Implementation Details

**PDF Processing (app.py:165-221)**
```python
def process_pdf(file_path: str, session_id: str) -> tuple[FAISS, int]:
    # Load PDF with page-level chunks
    md_text = pymupdf4llm.to_markdown(file_path, page_chunks=True)

    documents = []
    for item in md_text:  # List of page dicts
        page_num = item.get('metadata', {}).get('page', 1)
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

    # Split while preserving metadata
    chunks = text_splitter.split_documents(documents)

    # Create FAISS index
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(str(INDEX_DIR / session_id))

    return vectorstore, len(chunks)
```

**Relevance Checking (app.py:277-295)**
```python
def check_answer_in_context(question: str, context: str) -> bool:
    """LLM evaluates if context answers question"""
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
```

**Web Search (app.py:256-285)**
```python
def perform_web_search(question: str) -> List[WebSource]:
    """Tavily web search with format normalization"""
    results = tavily_search.invoke({"query": question})

    # Tavily returns dict with 'results' key
    if isinstance(results, dict):
        results_list = results.get('results', [])
    elif isinstance(results, list):
        results_list = results
    else:
        results_list = []

    web_sources = []
    for result in results_list[:MAX_WEB_SOURCES]:
        web_sources.append(WebSource(
            title=result.get('title', 'Untitled'),
            url=result.get('url', ''),
            snippet=result.get('content', result.get('snippet', ''))
        ))

    return web_sources
```

**Query Endpoint (app.py:382-454)**
```python
@app.post("/api/v1/query", response_model=QueryResponse)
async def query_notebook(request: QueryRequest):
    start_time = time.time()

    # Load vectorstore
    vectorstore = load_vectorstore(request.session_id)

    # Retrieve chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    chunks = retriever.invoke(request.question)

    # Build context
    context = "\n\n".join([chunk.page_content for chunk in chunks])

    # Check relevance with LLM
    can_answer_from_pdf = False
    if context.strip():
        can_answer_from_pdf = check_answer_in_context(request.question, context)

    if can_answer_from_pdf:
        # Answer from PDF
        chain = answer_prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": request.question})

        pdf_sources = build_pdf_sources(chunks)

        return QueryResponse(
            answer=answer,
            source="pdf",
            pdf_sources=pdf_sources,
            web_sources=None,
            chunks_used=len(chunks),
            processing_time=time.time() - start_time,
            metadata={"model": "gpt-4o-mini", "can_answer": True}
        )
    else:
        # Fallback to web
        web_sources = perform_web_search(request.question)

        if not web_sources:
            raise HTTPException(status_code=404, detail="No information found")

        web_context = "\n\n".join([
            f"Title: {src.title}\nURL: {src.url}\nContent: {src.snippet}"
            for src in web_sources
        ])

        chain = web_answer_prompt | llm | StrOutputParser()
        answer = chain.invoke({"question": request.question, "web_context": web_context})

        return QueryResponse(
            answer=answer,
            source="web",
            pdf_sources=None,
            web_sources=web_sources,
            chunks_used=None,
            processing_time=time.time() - start_time,
            metadata={"model": "gpt-4o-mini", "can_answer": False}
        )
```

### 8.3 Frontend Implementation

**Message Rendering with Markdown (index.html:133-139)**
```jsx
return (
    <div className="flex justify-start mb-4">
        <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 max-w-2xl">
            <div
                className="mb-2 markdown-content"
                dangerouslySetInnerHTML={{ __html: marked.parse(message.content || '') }}
            />

            {/* Badge */}
            {message.source && (
                <div className="mb-2">
                    <span className={`inline-flex items-center px-2 py-1 text-xs font-medium rounded ${
                        message.source === 'pdf'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-blue-100 text-blue-800'
                    }`}>
                        {message.source === 'pdf' ? 'From PDF' : 'From Web'}
                    </span>
                </div>
            )}

            {/* PDF Sources */}
            {message.pdfSources && message.pdfSources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="text-sm font-semibold text-gray-700 mb-2">PDF Sources:</div>
                    <ul className="space-y-1">
                        {message.pdfSources.map((src, idx) => (
                            <li key={idx} className="text-sm">
                                <a
                                    href={api.getPDFUrl(notebookId, src.file_name)}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:underline"
                                >
                                    📄 {src.file_name}
                                    {src.page_start && ` (pages ${src.page_start}${src.page_end !== src.page_start ? `-${src.page_end}` : ''})`}
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Web Sources */}
            {message.webSources && message.webSources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="text-sm font-semibold text-gray-700 mb-2">Web Sources:</div>
                    <ul className="space-y-2">
                        {message.webSources.map((src, idx) => (
                            <li key={idx} className="text-sm">
                                <a
                                    href={src.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:underline flex items-start"
                                >
                                    <span className="mr-1">🔗</span>
                                    <div>
                                        <div className="font-medium">{src.title}</div>
                                        <div className="text-gray-600 text-xs mt-1">{src.snippet}</div>
                                    </div>
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    </div>
);
```

**Delete Functionality (index.html:476-495)**
```jsx
<button
    onClick={async (e) => {
        e.stopPropagation();
        if (confirm(`Delete "${notebook.name}"?`)) {
            try {
                await api.deleteNotebook(notebook.id);
                fetchNotebooks();  // Refresh list
            } catch (error) {
                alert('Failed to delete: ' + error.message);
            }
        }
    }}
    className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity p-2 rounded-lg hover:bg-red-50 text-red-600"
    title="Delete notebook"
>
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
</button>
```

---

## 9. Performance & Quality

### 9.1 Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| PDF Upload (10 pages) | ≤ 15s | ~12s |
| Query Response (PDF) | ≤ 5s | ~3.5s |
| Query Response (Web) | ≤ 10s | ~7s |
| Memory Usage | < 2 GB | ~500 MB |
| First Paint | ≤ 2s | ~1s |

### 9.2 Error Handling

**Backend:**
- Global exception handler returns JSON: `{success: false, error: str, error_code: str}`
- HTTP 404 for missing resources
- HTTP 400 for invalid input
- HTTP 500 for server errors

**Frontend:**
- Try-catch on all API calls
- Alert for delete failures
- Error messages in chat for query failures
- Loading states during operations

### 9.3 Data Persistence

**SQLite Schema:**
```sql
CREATE TABLE notebooks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    sources_count INTEGER DEFAULT 1
);
```

**File Storage:**
```
data/
├── pdfs/
│   └── {session_id}/
│       └── {filename}.pdf
├── index/
│   └── {session_id}/
│       ├── index.faiss
│       └── index.pkl
└── db.sqlite
```

---

## 10. Acceptance Criteria

### AC-1: Notebook Management ✅
- [x] Home page displays all notebooks in grid
- [x] "Create new notebook" card always visible
- [x] Create modal validates name and PDF
- [x] New notebook appears in grid after creation
- [x] Delete button appears on hover
- [x] Delete confirmation required
- [x] Notebook removed from UI after deletion

### AC-2: PDF Chat ✅
- [x] Click notebook opens chat interface
- [x] Back button returns to home
- [x] Messages display with proper styling
- [x] User messages right-aligned, blue
- [x] Assistant messages left-aligned, white with border
- [x] Markdown renders correctly (headers, lists, code, etc.)

### AC-3: Source Attribution - PDF ✅
- [x] "From PDF" badge shows (green) when answer from PDF
- [x] PDF Sources section displays below answer
- [x] Each source shows: 📄 filename (pages X-Y)
- [x] Clicking source opens PDF in new tab
- [x] Page numbers accurate from metadata

### AC-4: Source Attribution - Web ✅
- [x] "From Web" badge shows (blue) when answer from web
- [x] Web Sources section displays below answer
- [x] Each source shows: 🔗 Title, URL, snippet
- [x] Clicking source opens webpage in new tab
- [x] Snippets provide context preview

### AC-5: Intelligent Routing ✅
- [x] LLM checks if PDF context answers question
- [x] PDF source used when relevant
- [x] Web search triggered when PDF insufficient
- [x] No false positives (irrelevant PDF triggering PDF source)
- [x] Tavily integration working correctly

### AC-6: UI/UX Polish ✅
- [x] Responsive grid layout
- [x] Hover effects on cards
- [x] Smooth transitions
- [x] Loading states during processing
- [x] Enter key sends message
- [x] Auto-scroll to latest message
- [x] Empty states shown appropriately

---

## Technical Summary

### Backend Architecture
- **Single-file FastAPI** (`app.py`) serving both API and frontend
- **PyMuPDF4LLM** for page-level PDF extraction with metadata
- **FAISS** vector store with local persistence
- **LLM-based relevance checking** for accurate source routing
- **Tavily web search** with format normalization
- **SQLite** for notebook metadata
- **Port 8000** for all services

### Frontend Architecture
- **Single-file React** (`index.html`) with CDN imports
- **Tailwind CSS + Flowbite** for styling
- **Marked.js** for markdown rendering
- **Babel Standalone** for JSX transpilation
- **Zero build step** - runs directly in browser

### Data Flow
1. **Upload**: PDF → PyMuPDF4LLM → Chunks → FAISS → Persist
2. **Query**: Question → Retrieve → LLM Check → PDF/Web → Sources → Response
3. **Render**: Response → Parse → Markdown → Badge → Sources → UI

### Key Differentiators
- **Accurate source detection** via LLM semantic check (not heuristics)
- **Complete source attribution** for both PDF and web
- **Single-port deployment** (backend serves frontend)
- **Zero-build architecture** (no webpack, no compilation)
- **Professional UI** with Tailwind + markdown support

---

## 11. Lessons Learned & Best Practices

### Critical Bug Fixes

**1. False Confidence from Vector Similarity**

**Problem:** FAISS always returns chunks, even when irrelevant. Text-length heuristics failed.

**Original (Broken) Logic:**
```python
def calculate_confidence(chunks):
    avg_length = sum(len(chunk.page_content) for chunk in chunks) / len(chunks)
    return min(avg_length / 500, 1.0)  # ❌ No semantic understanding
```

**Fixed with LLM Semantic Check:**
```python
def check_answer_in_context(question: str, context: str) -> bool:
    # LLM evaluates: "Can this context answer this question?"
    # Returns YES/NO based on semantic relevance
    # Added ~1-2s latency but eliminated false positives
```

**Key Insight:** Never trust vector similarity alone. Use LLM to validate semantic relevance.

---

**2. Tavily Response Format Mismatch**

**Problem:** Web search returned empty sources despite Tavily working.

**Root Cause:**
```python
# Expected: List
# Actual: Dict with 'results' key
{'query': '...', 'results': [...]}
```

**Fix:**
```python
if isinstance(results, dict):
    results_list = results.get('results', [])
elif isinstance(results, list):
    results_list = results
```

**Key Insight:** Always test API responses directly before writing parsing code. Don't assume formats.

---

### Architecture Decisions

**1. Single-File Design**
- ✅ 485 lines (backend) + 564 lines (frontend) = maintainable
- ✅ Zero build step = instant development
- ✅ Easy deployment = copy two files
- ❌ Limited scalability (acceptable for MVPs)

**2. Single-Port Deployment**
```python
@app.get("/")
async def serve_frontend():
    return FileResponse(str(FRONTEND_HTML))
```
- ✅ No CORS issues
- ✅ Single `python app.py` command
- ✅ Simplified security (same-origin)

**3. CDN-Based Frontend**
- ✅ No npm, no package.json, no build
- ✅ Works offline once cached
- ❌ Slower first load (acceptable tradeoff)

---

### RAG Implementation

**1. Metadata Preservation**
```python
# PyMuPDF4LLM extracts with page metadata
doc = Document(
    page_content=text,
    metadata={'file_name': '...', 'page_number': N}
)

# LangChain preserves metadata during split
chunks = text_splitter.split_documents(documents)
# Each chunk retains parent metadata!
```

**Key Insight:** Use `split_documents()` not `split_text()` to preserve metadata.

**2. Source Deduplication**
```python
# Same page can appear in multiple chunks
# Dedupe by file+page before showing user
key = f"{file_name}:{page_start}-{page_end}"
if key not in sources_dict:
    sources_dict[key] = PdfSource(...)
```

**3. FAISS Persistence**
```python
# Save
vectorstore.save_local(str(INDEX_DIR / session_id))

# Load (requires allow_dangerous_deserialization)
FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
```

---

### Frontend Best Practices

**1. Markdown Rendering**
```jsx
<div
    className="markdown-content"
    dangerouslySetInnerHTML={{ __html: marked.parse(content) }}
/>
```
- Safe here (content from our LLM, not user input)
- Simpler than MDX or react-markdown

**2. Source Attribution UI**
```jsx
// Visual indicators > verbose labels
📄 filename.pdf (pages 12)
🔗 Article Title - snippet preview
```

**3. Delete Confirmation**
```jsx
onClick={async (e) => {
    e.stopPropagation();  // Don't trigger parent
    if (confirm(`Delete "${name}"?`)) {
        await api.delete(id);
        refresh();
    }
}}
```

---

### Testing & Debugging

**1. Test API Responses Directly**
```python
# Before writing parsing code
python -c "
from langchain_tavily import TavilySearch
result = tavily_search.invoke({'query': 'test'})
print(type(result))  # Verify format
"
```

**2. Curl Testing**
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Query test
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"session_id":"...","question":"test"}'
```

**3. Error Logging**
```python
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()  # Always include traceback
    return []
```

---

### Security

**1. Path Sanitization**
```python
# User-provided filenames → sanitize
file_name = os.path.basename(file_name)  # Remove path traversal
pdf_path = PDFS_DIR / notebook_id / file_name
```

**2. Error Response Format**
```python
{
    "success": False,
    "error": str(exc),
    "error_code": "INTERNAL_ERROR"
}
```

---

### Performance Metrics

| Metric | Target | Achieved |
|--------|--------|----------|
| PDF Upload (10 pages) | ≤ 15s | ~12s |
| Query (PDF) | ≤ 5s | ~3.5s |
| Query (Web) | ≤ 10s | ~7s |
| Memory | < 2 GB | ~500 MB |

---

### Future Improvements

1. **Streaming responses** - Real-time answer generation
2. **Multi-PDF support** - Multiple PDFs per notebook
3. **Chat history** - Store conversation in SQLite
4. **Batch embeddings** - Faster PDF processing
5. **Async operations** - Parallel retrieval + relevance check
6. **PDF viewer** - In-browser viewing with highlighting

---

### Key Takeaways

1. **Semantic relevance > Text similarity** - Use LLM to validate context
2. **Test API responses directly** - Don't assume formats
3. **Preserve metadata everywhere** - Critical for attribution
4. **Simple architecture wins** - Single-file beats complex for MVPs
5. **Source transparency builds trust** - Always show where answers come from

**Total implementation:** ~8 hours | ~1,000 lines | 15 dependencies
