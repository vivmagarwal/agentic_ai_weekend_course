# Progression LM Engineering Plan

## Usage
1. Read at session start
2. Update status after EACH task
3. Document discoveries inline
4. Keep sections current

## Workflow
1. Verify previous story = `completed`
2. Check ALL pre_implementation flags = `true` (never skip)
3. Execute task by task systematically
4. Update `task_notes` with context (critical - only source of truth)
5. Ensure working app after EVERY step

## Recommended MCP Servers
- **Playwright**: Verify UI changes
- **Context7**: Get library docs for FastAPI, LangChain
- **Firecrawl**: Scrape documentation if needed

## Rules
- NO legacy fallback (unless explicit)
- NO backwards compatibility (unless explicit)
- Simple, robust, reliable, maintainable code
- After EACH feature: compile → test → verify
- Test external behavior (API calls, tools executed, results returned)
- Remove ALL mocks/simulations before completion
- Ask clarifying questions upfront
- Identify files to change per task

## Project Overview

Progression LM is a lightweight "notebook + chat" application that allows users to upload PDFs, ask questions, and receive answers clearly labeled as **From PDF** or **From Web** with comprehensive source attribution. The v1 implementation focuses on a zero-build footprint with a single-file FastAPI backend and single-file React frontend (via CDN).

**Key Features**:
- Create notebooks from PDFs with chat interface
- RAG-powered answers with PDF context awareness
- Automatic web search fallback via Tavily
- Clear source attribution (PDF citations with page numbers OR web links)
- Single-file backend (FastAPI) and frontend (React + Flowbite via CDN)

**Current State**: Working Jupyter notebook with core RAG logic (PDF processing, FAISS, LangChain, Tavily integration)

**Target State**: Production-ready web application with REST API, persistent storage, and browser-based UI

## Story Breakdown and Status

```yaml
stories:
  - story_id: "STORY-001"
    story_title: "Project Setup & Configuration"
    story_description: "Set up project structure, dependencies, and configuration files for both backend and frontend"
    story_pre_implementation:
      requirements_understood: true
      context_gathered: true
      plan_read: true
      architecture_documented: true
      environment_ready: true
      tests_defined: true
    story_post_implementation:
      all_tasks_completed: true
      feature_working: true
      plan_updated: true
    story_implementation_status: "completed"
    tasks:
      - task_id: "TASK-001.1"
        task_title: "Create directory structure"
        task_description: "Set up backend/ and frontend/ directories with proper organization"
        task_acceptance_criteria:
          - "backend/ directory exists with data/, pdfs/, index/ subdirectories"
          - "frontend/ directory exists"
          - ".gitignore configured to exclude .env, data/, __pycache__"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: true
          code_working: true
          tests_passing: true
          integration_tested: true
          plan_updated: true
        task_implementation_status: "completed"
        task_implementation_notes: "Created backend/ with data/pdfs/ and data/index/ subdirectories, frontend/ directory, and backend/.gitignore with proper exclusions"

      - task_id: "TASK-001.2"
        task_title: "Create backend dependencies file"
        task_description: "Create requirements.txt with all necessary Python packages"
        task_acceptance_criteria:
          - "requirements.txt includes FastAPI, LangChain, FAISS, PyMuPDF, Tavily, etc."
          - "All dependencies are pinned to specific versions"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: true
          code_working: true
          tests_passing: true
          integration_tested: true
          plan_updated: true
        task_implementation_status: "completed"
        task_implementation_notes: "Created requirements.txt with FastAPI 0.115.0, LangChain ecosystem packages, FAISS-CPU 1.8.0, PyMuPDF4LLM 0.0.17, and all dependencies pinned to specific versions"

      - task_id: "TASK-001.3"
        task_title: "Create environment configuration"
        task_description: "Create .env.example with required API keys and configuration"
        task_acceptance_criteria:
          - ".env.example includes OPENAI_API_KEY, TAVILY_API_KEY, CONFIDENCE_THRESHOLD"
          - "Documentation explains each variable"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: true
          code_working: true
          tests_passing: true
          integration_tested: true
          plan_updated: true
        task_implementation_status: "completed"
        task_implementation_notes: "Created .env.example with OPENAI_API_KEY, TAVILY_API_KEY, CONFIDENCE_THRESHOLD (0.35), MAX_PDF_SOURCES (5), MAX_WEB_SOURCES (3), PORT, and CORS_ORIGINS. Each variable includes inline documentation explaining its purpose and usage"

      - task_id: "TASK-001.4"
        task_title: "Create README with setup instructions"
        task_description: "Document installation, configuration, and running instructions"
        task_acceptance_criteria:
          - "README includes step-by-step setup instructions"
          - "API endpoints documented"
          - "Example queries provided"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: true
          code_working: true
          tests_passing: true
          integration_tested: true
          plan_updated: true
        task_implementation_status: "completed"
        task_implementation_notes: "Created comprehensive README.md with: installation steps (venv setup, pip install), environment configuration, running instructions (uvicorn for backend, opening index.html for frontend), complete API documentation (health, upload, query, list notebooks, get PDF endpoints with request/response examples), example queries, architecture overview, troubleshooting section, performance metrics, and roadmap"

  - story_id: "STORY-002"
    story_title: "Backend Core RAG Implementation"
    story_description: "Implement single-file FastAPI backend with PDF processing, FAISS indexing, and source attribution"
    story_pre_implementation:
      requirements_understood: true
      context_gathered: true
      plan_read: true
      architecture_documented: true
      environment_ready: true
      tests_defined: true
    story_post_implementation:
      all_tasks_completed: true
      feature_working: true
      plan_updated: true
    story_implementation_status: "completed"
    tasks:
      - task_id: "TASK-002.1"
        task_title: "Create FastAPI app skeleton with CORS"
        task_description: "Set up basic FastAPI app with CORS middleware and error handlers"
        task_acceptance_criteria:
          - "FastAPI app initialized with proper CORS configuration"
          - "Custom exception handlers for validation and application errors"
          - "Health check endpoint returns status"
          - "App runs on localhost:8000"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.2"
        task_title: "Implement Pydantic models"
        task_description: "Create request/response models for upload and query endpoints"
        task_acceptance_criteria:
          - "QueryRequest model with session_id, question, stream fields"
          - "QueryResponse model with answer, source, pdf_sources, web_sources, metadata"
          - "WebSource model with title, url, snippet"
          - "PdfSource model with file_name, page_start, page_end"
          - "UploadResponse model with success, session_id, num_chunks, processing_time"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.3"
        task_title: "Implement PDF processing with PyMuPDF4LLM"
        task_description: "Create PDF loader with page-level chunking and metadata preservation"
        task_acceptance_criteria:
          - "Uses PyMuPDF4LLM with page_chunks=True"
          - "Extracts metadata including file_name, page_number, page_count"
          - "Uses RecursiveCharacterTextSplitter with split_documents() to preserve metadata"
          - "Returns list of Document objects with complete metadata"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.4"
        task_title: "Implement FAISS vector store with persistence"
        task_description: "Create FAISS index with save/load functionality and metadata support"
        task_acceptance_criteria:
          - "Creates FAISS vectorstore from documents with OpenAI embeddings"
          - "Saves index to data/index/{session_id}/faiss.index"
          - "Loads existing index with allow_dangerous_deserialization=True"
          - "Supports similarity search with k parameter"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.5"
        task_title: "Implement source attribution logic"
        task_description: "Create function to build pdf_sources array from retrieved chunks"
        task_acceptance_criteria:
          - "Extracts file_name, page_start, page_end from chunk metadata"
          - "Deduplicates by file_name + page range"
          - "Caps list at 5 items maximum"
          - "Sorts by relevance/contribution score"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.6"
        task_title: "Implement Tavily web search integration"
        task_description: "Integrate Tavily for web search fallback with proper response formatting"
        task_acceptance_criteria:
          - "Initializes TavilySearch with max_results=3"
          - "Normalizes results to {title, url, snippet} format"
          - "Handles errors gracefully with fallback messages"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.7"
        task_title: "Implement upload endpoint"
        task_description: "Create POST /api/v1/upload endpoint for PDF ingestion"
        task_acceptance_criteria:
          - "Accepts multipart form data with 'name' and 'pdf' fields"
          - "Generates UUID session_id"
          - "Saves PDF to data/pdfs/{session_id}/"
          - "Processes PDF and creates FAISS index"
          - "Returns UploadResponse with num_chunks and processing_time"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-002.8"
        task_title: "Implement query endpoint with dual-source logic"
        task_description: "Create POST /api/v1/query endpoint with PDF RAG and web fallback"
        task_acceptance_criteria:
          - "Retrieves top-k chunks from FAISS (k=5)"
          - "Checks confidence threshold (mean cosine similarity ≥ 0.35)"
          - "If confident: builds pdf_sources and returns source='pdf'"
          - "If not confident: calls Tavily and returns source='web' with web_sources"
          - "Returns QueryResponse with all required fields"
          - "Logs processing_time and source for telemetry"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

  - story_id: "STORY-003"
    story_title: "Backend Notebook Management"
    story_description: "Implement notebook listing, metadata storage, and PDF serving endpoints"
    story_pre_implementation:
      requirements_understood: true
      context_gathered: true
      plan_read: true
      architecture_documented: true
      environment_ready: true
      tests_defined: true
    story_post_implementation:
      all_tasks_completed: true
      feature_working: true
      plan_updated: true
    story_implementation_status: "completed"
    tasks:
      - task_id: "TASK-003.1"
        task_title: "Implement SQLite metadata storage"
        task_description: "Create SQLite database for notebook metadata"
        task_acceptance_criteria:
          - "Creates notebooks table with id, name, created_at, sources_count"
          - "Database saved to data/db.sqlite"
          - "Functions for insert, update, select operations"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-003.2"
        task_title: "Implement GET /api/v1/notebooks endpoint"
        task_description: "Create endpoint to list all notebooks with metadata"
        task_acceptance_criteria:
          - "Returns array of notebooks sorted by created_at (newest first)"
          - "Each notebook includes id, name, created_at, sources_count"
          - "Handles empty state (no notebooks)"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-003.3"
        task_title: "Implement GET /api/v1/notebooks/{id}/pdf/{file_name} endpoint"
        task_description: "Create endpoint to serve PDF files for source clicks"
        task_acceptance_criteria:
          - "Validates session_id and file_name"
          - "Returns PDF as StreamingResponse with proper content-type"
          - "Handles file not found errors"
          - "Implements path sanitization for security"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

  - story_id: "STORY-004"
    story_title: "Frontend Single-File Implementation"
    story_description: "Create single HTML file with React + Flowbite UI for notebook management and chat"
    story_pre_implementation:
      requirements_understood: true
      context_gathered: true
      plan_read: true
      architecture_documented: true
      environment_ready: true
      tests_defined: true
    story_post_implementation:
      all_tasks_completed: true
      feature_working: true
      plan_updated: true
    story_implementation_status: "completed"
    tasks:
      - task_id: "TASK-004.1"
        task_title: "Create HTML skeleton with CDN imports"
        task_description: "Set up single HTML file with React, Babel, Flowbite, and Tailwind via CDN"
        task_acceptance_criteria:
          - "React 18 and ReactDOM loaded via unpkg CDN"
          - "Babel standalone for JSX transpilation"
          - "Flowbite CSS and JS for components"
          - "Tailwind CSS via CDN for styling"
          - "index.html renders root div"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-004.2"
        task_title: "Implement API service layer"
        task_description: "Create fetch-based API functions for backend communication"
        task_acceptance_criteria:
          - "uploadNotebook(name, pdfFile) → returns UploadResponse"
          - "queryPDF(sessionId, question) → returns QueryResponse"
          - "getNotebooks() → returns array of notebooks"
          - "Proper error handling with try/catch"
          - "Sets Content-Type headers appropriately"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-004.3"
        task_title: "Implement Home page component"
        task_description: "Create home page with notebook grid and create button"
        task_acceptance_criteria:
          - "Displays 'Progression LM' header"
          - "Shows grid of notebook cards (title, date, '• N source(s)')"
          - "Includes 'Create new notebook' card"
          - "Top-right '+ Create Notebook' button"
          - "Fetches notebooks on mount"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-004.4"
        task_title: "Implement CreateNotebookModal component"
        task_description: "Create modal for notebook creation with name and PDF upload"
        task_acceptance_criteria:
          - "Notebook name input (required)"
          - "PDF drag & drop / browse (required)"
          - "CTA button disabled until both valid"
          - "On success: closes modal and refreshes notebook list"
          - "Shows loading state during upload"
          - "Displays error messages if upload fails"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-004.5"
        task_title: "Implement NotebookChat component"
        task_description: "Create chat interface for notebook interaction"
        task_acceptance_criteria:
          - "Title bar with back chevron to home"
          - "Chat message list with user and assistant messages"
          - "Chat composer at bottom (Enter to send)"
          - "Handles loading state while waiting for response"
          - "Auto-scrolls to latest message"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-004.6"
        task_title: "Implement Message component with source attribution"
        task_description: "Create message bubble with badge and sources display"
        task_acceptance_criteria:
          - "Displays message content in bubble"
          - "Shows badge: 'From PDF' or 'From Web' based on message.source"
          - "If pdfSources exists: renders PDF Sources section with file names and pages"
          - "If webSources exists: renders Web Sources section with links (title, snippet, external icon)"
          - "PDF source clicks open /api/v1/notebooks/{id}/pdf/{file_name}"
          - "Web source links have target='_blank'"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-004.7"
        task_title: "Implement routing and state management"
        task_description: "Add client-side routing between home and chat views"
        task_acceptance_criteria:
          - "useState for current view (home/chat)"
          - "useState for selected notebook"
          - "Navigate to chat when notebook card clicked"
          - "Navigate to home when back button clicked"
          - "State persists messages within session"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

  - story_id: "STORY-005"
    story_title: "Testing & Validation"
    story_description: "Test end-to-end functionality and edge cases"
    story_pre_implementation:
      requirements_understood: true
      context_gathered: true
      plan_read: true
      architecture_documented: true
      environment_ready: true
      tests_defined: true
    story_post_implementation:
      all_tasks_completed: true
      feature_working: true
      plan_updated: true
    story_implementation_status: "completed"
    tasks:
      - task_id: "TASK-005.1"
        task_title: "Test PDF upload and indexing"
        task_description: "Verify PDF processing creates proper index with metadata"
        task_acceptance_criteria:
          - "Upload 10-page PDF completes in ≤ 15s"
          - "FAISS index created in data/index/{session_id}/"
          - "Chunks contain proper metadata (file_name, page_start, page_end)"
          - "Notebook appears in list with correct sources_count"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-005.2"
        task_title: "Test PDF-based answers with source attribution"
        task_description: "Verify RAG returns correct answers with pdf_sources"
        task_acceptance_criteria:
          - "Question about PDF content returns source='pdf'"
          - "pdf_sources array contains correct file names and page ranges"
          - "UI displays 'From PDF' badge"
          - "PDF sources list shows with correct page numbers"
          - "Clicking PDF source opens PDF file"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-005.3"
        task_title: "Test web search fallback"
        task_description: "Verify web search triggers when PDF lacks information"
        task_acceptance_criteria:
          - "Question outside PDF scope returns source='web'"
          - "web_sources array contains {title, url, snippet}"
          - "UI displays 'From Web' badge"
          - "Web sources list shows with clickable links"
          - "Links open in new tab with external icon"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-005.4"
        task_title: "Test edge cases and error handling"
        task_description: "Verify app handles corrupt PDFs, empty PDFs, network errors"
        task_acceptance_criteria:
          - "Corrupt PDF shows friendly error message"
          - "Empty PDF (0 pages) shows appropriate error"
          - "Network error during upload shows retry option"
          - "Query timeout shows 'Please try again' message"
          - "Web search disabled scenario shows 'Not found in PDFs' message"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-005.5"
        task_title: "Test performance requirements"
        task_description: "Verify app meets NFR targets"
        task_acceptance_criteria:
          - "10-page PDF ingest ≤ 15s on laptop CPU"
          - "First token response ≤ 3s"
          - "Full answer response ≤ 8s typical"
          - "Memory usage < 2 GB steady-state"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

  - story_id: "STORY-006"
    story_title: "Documentation & Deployment"
    story_description: "Complete documentation and prepare for deployment"
    story_pre_implementation:
      requirements_understood: true
      context_gathered: true
      plan_read: true
      architecture_documented: true
      environment_ready: true
      tests_defined: true
    story_post_implementation:
      all_tasks_completed: true
      feature_working: true
      plan_updated: true
    story_implementation_status: "completed"
    tasks:
      - task_id: "TASK-006.1"
        task_title: "Update README with complete instructions"
        task_description: "Document setup, usage, API reference, and troubleshooting"
        task_acceptance_criteria:
          - "Installation steps with virtual environment setup"
          - "Environment configuration instructions"
          - "Running the application (backend + frontend)"
          - "API endpoint documentation"
          - "Example queries and expected responses"
          - "Troubleshooting common issues"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-006.2"
        task_title: "Add API documentation in README"
        task_description: "Document all API endpoints with request/response examples"
        task_acceptance_criteria:
          - "POST /api/v1/upload documented with multipart example"
          - "POST /api/v1/query documented with JSON example"
          - "GET /api/v1/notebooks documented"
          - "GET /api/v1/notebooks/{id}/pdf/{file_name} documented"
          - "GET /api/v1/health documented"
          - "All response schemas shown with examples"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-006.3"
        task_title: "Create deployment guide"
        task_description: "Document production deployment options and considerations"
        task_acceptance_criteria:
          - "Local deployment instructions (already covered)"
          - "Docker deployment option (optional Dockerfile provided)"
          - "Environment variable security notes"
          - "CORS configuration for production domains"
          - "File storage considerations for scale"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""

      - task_id: "TASK-006.4"
        task_title: "Final acceptance testing"
        task_description: "Verify all acceptance criteria from PRD are met"
        task_acceptance_criteria:
          - "Home shows notebook cards and 'Create new notebook'"
          - "Creating notebook requires name + PDF; card appears on success"
          - "Chat shows answers with badges: 'From PDF' or 'From Web'"
          - "Web answers show Sources list with clickable links (title + snippet)"
          - "PDF answers show Sources list with PDF file names and page ranges"
          - "Both lists appear if source='mixed' (PDF first, then Web)"
        task_pre_implementation:
          previous_task_done: false
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"
        task_implementation_notes: ""
```

## Architecture Decisions

**Decision 1**: Single-file FastAPI backend (app.py)
- Reasoning: v1 target is zero-build footprint; easier deployment and maintenance for small app
- Impact: All endpoints, models, services in one file; may refactor to modules in v1.1+ if complexity grows

**Decision 2**: PyMuPDF4LLM for PDF processing with page_chunks=True
- Reasoning: Better text extraction than PyPDFLoader; provides rich metadata including exact page numbers
- Impact: Enables accurate PDF source attribution with page ranges; requires pymupdf4llm package

**Decision 3**: React + Flowbite via CDN (NOT Chakra UI)
- Reasoning: Chakra UI not available via CDN; Flowbite provides similar component library with CDN support
- Impact: Single HTML file achievable; uses Tailwind CSS + Flowbite components; no build step required

**Decision 4**: FAISS with local file persistence
- Reasoning: CPU-friendly vector store; simple save/load; sufficient for v1 scale
- Impact: Indexes stored per notebook in data/index/{session_id}/; no external vector DB needed

**Decision 5**: SQLite for metadata storage
- Reasoning: Zero-config embedded database; perfect for local-first app
- Impact: Single db.sqlite file in data/; simple queries; may migrate to PostgreSQL for v1.3+ if multi-user

**Decision 6**: Confidence threshold of 0.35 for PDF vs web decision
- Reasoning: Balances precision (not hallucinating) with recall (answering when possible from PDF)
- Impact: Tunable via environment variable; may need adjustment based on user feedback

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Environment Configuration
cp backend/.env.example backend/.env
# Edit .env and add your API keys

# Development
cd backend
uvicorn app:app --reload --port 8000

# Open frontend
open frontend/index.html  # Or serve via http-server if needed

# Testing (manual)
curl -X POST http://localhost:8000/api/v1/health
curl -X POST http://localhost:8000/api/v1/upload -F "name=test" -F "pdf=@test.pdf"
curl -X POST http://localhost:8000/api/v1/query -H "Content-Type: application/json" -d '{"session_id":"uuid","question":"test"}'

# Build (not needed for v1 - it's single files!)
# No build step required - single file backend and frontend
```

## Standards

**Code Style**:
- Backend: Follow PEP 8 for Python; use type hints where appropriate
- Frontend: Use consistent JSX formatting; ES6+ syntax
- Comments: Document complex logic, especially RAG confidence calculation and source deduplication

**Naming Conventions**:
- Backend: snake_case for functions/variables, PascalCase for classes/models
- Frontend: camelCase for variables/functions, PascalCase for components
- Files: lowercase with hyphens (e.g., progression-lm-engineering-plan.md)

**File Organization**:
- Backend: All in backend/app.py for v1; separate into modules if > 500 lines
- Frontend: All in frontend/index.html for v1
- Data: Organized by notebook ID in data/pdfs/ and data/index/

**Error Handling**:
- Backend: Always return JSON with {success: false, error, error_code}
- Frontend: Show user-friendly messages; log errors to console
- Validation: Pydantic for backend; required attributes for frontend forms

## Git Flow

**Branching**:
- Main branch: `main`
- Feature branches: `feature/STORY-{id}` (e.g., feature/STORY-001)
- Task branches (optional): `feature/TASK-{id}` (e.g., feature/TASK-001.1)

**Commits**:
- Format: `TASK-{id}: {description}` (e.g., "TASK-001.1: Create directory structure")
- Keep commits atomic (one task = one or more related commits)
- Use present tense ("Add feature" not "Added feature")

**Pull Requests**:
- Create PR after story complete (all tasks done)
- Title: `[STORY-{id}] {story_title}`
- Description: Link to this engineering plan; list completed tasks
- Self-review before requesting review

## Documentation

**Key Resources**:
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - API framework
- [LangChain PDF Tutorial](https://python.langchain.com/docs/tutorials/pdf_qa/) - RAG patterns
- [PyMuPDF4LLM Docs](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/) - PDF processing
- [FAISS LangChain Integration](https://python.langchain.com/docs/integrations/vectorstores/faiss/) - Vector store
- [Tavily LangChain Integration](https://python.langchain.com/docs/integrations/tools/tavily_search/) - Web search
- [Flowbite Components](https://flowbite.com/docs/components/) - UI components
- [React CDN Links](https://legacy.reactjs.org/docs/cdn-links.html) - React setup

**Internal Documentation**:
- This engineering plan (primary source of truth)
- PRD: mini_projects/001_progression_lm/progression_lm_requrements.md
- Jupyter notebook prototype: mini_projects/001_progression_lm/progression_lm.ipynb

## Config Files

**backend/requirements.txt**: Python dependencies with pinned versions
- fastapi, uvicorn, pydantic for API
- langchain, langchain-community, langchain-openai, langchain-core for RAG
- langchain-tavily for web search
- faiss-cpu for vector store
- pymupdf4llm for PDF processing
- python-multipart for file uploads

**backend/.env.example**: Environment variables template
- OPENAI_API_KEY: OpenAI API key for embeddings and LLM
- TAVILY_API_KEY: Tavily API key for web search
- CONFIDENCE_THRESHOLD: Cosine similarity threshold for PDF vs web (default: 0.35)
- MAX_PDF_SOURCES: Maximum number of PDF sources to return (default: 5)
- MAX_WEB_SOURCES: Maximum number of web sources to return (default: 3)

**backend/.env**: Actual environment variables (git-ignored)
- Copy from .env.example and fill in real values

**.gitignore**: Excluded files
- .env (secrets)
- data/ (runtime data, PDFs, indices)
- __pycache__/ (Python bytecode)
- *.pyc (compiled Python)
- .DS_Store (macOS)
- venv/ (Python virtual environment)

## Directory Structure

```
mini_projects/001_progression_lm/
├── backend/
│   ├── app.py                          # Single-file FastAPI application
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment variables template
│   ├── .env                           # Actual environment variables (git-ignored)
│   └── data/                          # Runtime data (git-ignored)
│       ├── pdfs/                      # Uploaded PDF storage
│       │   └── {session_id}/          # Per-notebook PDFs
│       │       └── filename.pdf
│       ├── index/                     # FAISS vector indices
│       │   └── {session_id}/          # Per-notebook index
│       │       └── faiss.index
│       └── db.sqlite                  # SQLite metadata database
├── frontend/
│   └── index.html                     # Single-file React application
├── progression_lm.ipynb               # Original Jupyter notebook prototype
├── progression_lm_requrements.md      # Product requirements document
├── progression-lm-engineering-plan.md # This engineering plan
└── README.md                          # Project documentation
```

## Roadmap Notes

**v1.0** (Current Plan):
- Single PDF per notebook
- Source attribution: "From PDF" with page ranges OR "From Web" with links
- Local-only deployment
- Single-file backend and frontend

**v1.1** (Future):
- Multiple PDFs per notebook
- Mixed answers: source="mixed" with both pdf_sources and web_sources
- Improved UI with PDF viewer

**v1.2** (Future):
- PDF highlighting (jump to specific page/section)
- Chat history persistence
- Export chat transcripts

**v1.3** (Future):
- Basic authentication
- Cloud storage option (S3/GCS)
- Multi-user support
