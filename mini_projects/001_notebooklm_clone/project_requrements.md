# Progression LM — Product Requirements (with technical details)

A lightweight “notebook + chat” app. People upload PDFs, ask questions, and get answers that are clearly labeled **From PDF** or **From Web**, with sources shown right under the answer.

---

Backend sends `source` and optional `web_sources`; frontend renders the **From PDF / From Web** badge and a Sources list for web results. 

---

## 1) Goals

* Create notebooks from PDFs and chat inside each notebook.
* Always show where an answer came from:

  * **From PDF** → citations to the PDF(s)
  * **From Web** → clickable links
* Zero-build footprint option:

  * **BE**: all FastAPI in a single file (v1 target)
  * **FE**: a single HTML file with React + Chakra via CDNs

## 2) Non-Goals (v1)

* Auth, sharing, multi-user.
* File types other than PDF.
* In-PDF annotations.

---

## 3) Primary user stories

1. I can see my notebooks and create a new one (name + PDF).
2. I can open a notebook and chat.
3. If the answer is grounded in my PDFs, I see **From PDF** and the PDF sources.
4. If it’s not in my PDFs, the app falls back to the web and shows **From Web** with linked sources.
5. I can click sources to verify.

---

## 4) UX & flows

### 4.1 Home

* Header: **Progression LM**
* Grid:

  * “Create new notebook” card
  * Notebook cards (Title, date, “• N source(s)”)
* Top-right: **+ Create Notebook**

### 4.2 Create notebook modal

* Inputs:

  * **Notebook name** (required)
  * **PDF** drag & drop / browse (required)
* CTA disabled until both are valid.
* On success, a new card appears.

### 4.3 Notebook chat

* Title bar with back chevron.
* Chat composer at bottom (Enter to send).
* Each AI message:

  * Answer bubble
  * A small badge: **From PDF** or **From Web**
  * **Sources** section:

    * **From PDF** → list of PDFs (and page ranges)
    * **From Web** → list of links (title + snippet + external-link icon)

**Empty/edge states**

* Web disabled and no PDF hit → “Not found in your PDFs.”
* Corrupt/empty PDF → friendly error.

---

## 5) Source attribution (end-to-end)

### 5.1 What the code does today (from your repo)

**Backend (FastAPI)**

* `backend/app/api/v1/endpoints/query.py`

  * `POST /api/v1/query` returns a `QueryResponse` with:

    * `answer: string`
    * `source: 'pdf' | 'web'`
    * `web_sources?: Array<{title, url, snippet}>` (present when `source==='web'`)
    * `chunks_used?: number` (present when `source==='pdf'`)
* `backend/app/services/rag_service.py`

  * Tries PDF RAG first; if not confident, falls back to web (Tavily).
  * Normalizes **web results** into `{ title, url, snippet }[]`.
* `backend/app/models/response.py`

  * Pydantic models: `QueryResponse`, `WebSource`, etc.

**Frontend (React + Chakra)**

* `frontend/src/services/api.ts`

  * `queryPDF(sessionId, question)` calls `/api/v1/query` and returns the `QueryResponse`.
* `frontend/src/hooks/useChat.ts`

  * Maps BE shape to `Message`:

    * `message.source = data.source`
    * `message.webSources = data.web_sources ?? []`
* `frontend/src/components/Message.tsx`

  * Renders the badge:

    * `From PDF` if `message.source==='pdf'`
    * `From Web` if `message.source==='web'`
  * If `message.webSources.length > 0`, shows a **Sources** list with Chakra `Link` + `ExternalLinkIcon`.

**Gap**

* PDF answers don’t yet include a per-PDF list; FE can’t show PDF citations.

### 5.2 Target data contract (adds `pdf_sources`)

**Response (BE → FE)**

```json
{
  "success": true,
  "answer": "string",
  "source": "pdf" | "web" | "mixed",
  "pdf_sources": [
    { "file_name": "doc.pdf", "page_start": 3, "page_end": 4 }
  ],
  "web_sources": [
    { "title": "France | Britannica", "url": "https://...", "snippet": "..." }
  ],
  "chunks_used": 7,
  "processing_time": 1.23,
  "metadata": { "model": "gpt-4o-mini", "tokens": 1234 }
}
```

**Rules**

* `source="pdf"` → fill `pdf_sources`, omit/empty `web_sources`.
* `source="web"` → fill `web_sources`, omit/empty `pdf_sources`.
* `source="mixed"` (optional) → include both arrays; FE renders in two subsections in order: **PDF**, then **Web**.

---

## 6) Technical spec

### 6.1 Backend (single-file FastAPI target)

**Responsibilities**

* Upload & ingest PDF: extract text → chunk → embed → index.
* Chat:

  1. Retrieve top-k chunks from the notebook index.
  2. If above threshold → answer with PDF context; build `pdf_sources` from chunk metadata.
  3. Else → web search; build `web_sources` with `{title,url,snippet}`.
  4. Return `QueryResponse` (see contract above).

**Important details**

* **Chunk metadata** must include:

  * `file_name`, `page_start`, `page_end` (or approximate)
* **Citation assembly**:

  * Deduplicate by `file_name` + page range.
  * Cap list (e.g., top 5) to keep UI tidy.
* **Thresholds**:

  * Cosine similarity mean ≥ `0.35` (tunable).
* **Models**:

  * Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (CPU-friendly) or API.
  * LLM: pluggable (OpenAI/Anthropic/local), with sensible timeouts.

**Suggested layout for single-file `app.py`**

* `create_app()` sets up routes:

  * `POST /api/v1/upload`
  * `POST /api/v1/query`
  * `GET /api/v1/health`
* File storage:

  * PDFs → `/data/pdfs/{notebook_id}/...`
  * Index → `/data/index/{notebook_id}/faiss.index`
  * Meta (SQLite) → `/data/db.sqlite`
* Web search provider behind an interface (Tavily/Bing/SerpAPI).
* Logging each query with `source` and `processing_time`.

**Pseudocode for the query path**

```python
@router.post("/api/v1/query")
def query(req: QueryRequest) -> QueryResponse:
    chunks = index.retrieve(req.question, top_k=5)
    if confident(chunks):
        answer = llm.answer(context=concat(chunks), question=req.question)
        pdf_sources = summarize_sources(chunks)  # [{file_name, page_start, page_end}]
        return QueryResponse(
            success=True, answer=answer, source="pdf",
            pdf_sources=pdf_sources, chunks_used=len(chunks),
            processing_time=secs, metadata=meta
        )
    web = web_search(req.question)  # [{title,url,snippet}]
    answer = llm.answer(context=concat(web.snippets), question=req.question)
    return QueryResponse(
        success=True, answer=answer, source="web",
        web_sources=web, processing_time=secs, metadata=meta
    )
```

### 6.2 Frontend (single HTML with React + Chakra via CDNs)

**Responsibilities**

* Fetch notebooks, create notebook (upload), chat in a notebook.
* Render messages with:

  * Badge: **From PDF** / **From Web**
  * Sources panel:

    * For `pdf_sources`: file name + page range; clicking opens `/api/v1/notebooks/{id}/pdf/{file_name}` (or a `/files/{...}` route).
    * For `web_sources`: external link with `target="_blank"` and a short snippet.

**Data types (FE)**

```ts
type WebSource = { title: string; url: string; snippet: string };
type PdfSource = { file_name: string; page_start?: number; page_end?: number };

type QueryResponse = {
  success: boolean;
  answer: string;
  source: 'pdf' | 'web' | 'mixed';
  pdf_sources?: PdfSource[];
  web_sources?: WebSource[];
  chunks_used?: number;
  processing_time: number;
  metadata: { model: string; tokens?: number };
};

type Message = {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  source?: 'pdf' | 'web' | 'mixed';
  pdfSources?: PdfSource[];
  webSources?: WebSource[];
  timestamp: Date;
};
```

**Mapping (FE)**

```ts
const { data } = await api.query(sessionId, question);
messages.push({
  id: nanoid(),
  type: 'assistant',
  content: data.answer,
  source: data.source,
  pdfSources: data.pdf_sources ?? [],
  webSources: data.web_sources ?? [],
  timestamp: new Date(),
});
```

**Rendering (FE)**

* Badge:

  * `source==='pdf'` → `<Badge>From PDF</Badge>`
  * `source==='web'` → `<Badge>From Web</Badge>`
  * `source==='mixed'` → `<Badge>From PDF & Web</Badge>` (optional)
* Sources section:

  * If `pdfSources.length > 0` → “**Sources**” → subhead “PDF” → list of files (click to open).
  * If `webSources.length > 0` → “**Sources**” → subhead “Web” → list of links (`<a target="_blank">` + external icon).

**Single-file HTML skeleton**

```html
<link rel="stylesheet" href="https://unpkg.com/@chakra-ui/react/dist/chakra-ui.min.css">
<div id="root"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@chakra-ui/react@latest/dist/chakra-ui.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@emotion/react@latest/dist/emotion-react.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@emotion/styled@latest/dist/emotion-styled.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/framer-motion/dist/framer-motion.umd.js"></script>

<script>
  // minimal render of Message with badge + sources using Chakra
</script>
```

---

## 7) API design

### `POST /api/v1/upload`  *(multipart)*

* Form fields: `name`, `pdf`
* Returns:

```json
{
  "success": true,
  "message": "Uploaded",
  "session_id": "uuid",
  "filename": "my.pdf",
  "num_chunks": 123,
  "processing_time": 3.1
}
```

### `POST /api/v1/query`

* Body:

```json
{ "session_id": "uuid", "question": "string", "stream": false }
```

* Returns: **QueryResponse** (see above).

### `GET /api/v1/notebooks` *(optional for home grid)*

* Returns last N notebooks with `sources_count`.

### `GET /api/v1/notebooks/{id}/pdf/{file_name}`

* Streams the PDF file for the source click.

---

## 8) Performance & NFRs

* Ingest 10-page PDF ≤ 15s on laptop CPU.
* First token ≤ 3s; whole answer ≤ 8s typical.
* Memory steady-state < 2 GB.
* Errors return JSON `{ success:false, error, error_code }`.

---

## 9) Security & Privacy

* Local-only by default; CORS restricted to `localhost`.
* Log IDs and timings, not raw content.
* File path sanitization on upload.

---

## 10) Telemetry

* Events: `notebook_created`, `ingest_complete`, `chat_asked`, `answer_source`, `processing_time`.
* Counters drive the “Recent Notebooks” list.

---

## 11) Acceptance criteria

1. Home shows notebook cards and “Create new notebook”.
2. Creating a notebook requires name + PDF; on success a card appears with “• N source(s)”.
3. Chat shows answers with badges: **From PDF** for RAG, **From Web** for fallback.
4. **Web** answers show a Sources list with clickable links (title + snippet).
5. **PDF** answers show a Sources list with PDF file names and page ranges.
6. If both contribute, both lists appear (PDF first).

---

## 12) Implementation hints

* **Backend**

  * Keep per-chunk metadata: `{file_name, page_start, page_end}`.
  * When assembling `pdf_sources`, dedupe on `file_name+page_range`.
  * Cap lists to 5 items; sort by contribution score.
  * If using LangChain: store these in each `Document.metadata`.

* **Frontend**

  * When `pdfSources` exist, render a “PDF” subheader under **Sources**.
  * For PDFs: link to `/api/v1/notebooks/{id}/pdf/{file_name}`; for Web: `target="_blank"`.
  * Use Chakra `Badge`, `VStack`, `Link`, and `Divider` to match screenshots.

---

## 13) Roadmap

* **1.0**: single-file BE + single-file FE; web fallback; **From Web** sources; **From PDF** badge.
* **1.1**: **`pdf_sources`** wired end-to-end; mixed answers.
* **1.2**: Multiple PDFs per notebook; PDF viewer with page highlighting.
* **1.3**: Basic auth; cloud storage option.

---

### Quick diff checklist (to ship PDF citations)

* [ ] BE: add `pdf_sources` to `QueryResponse` and populate from chunk metadata.
* [ ] FE: surface `pdf_sources` on messages and render a PDF Sources list.
* [ ] Route to serve PDFs for clicks.
* [ ] Tests: one BE unit for `pdf_sources`, one FE render test.

This PRD keeps your current behavior (badges + web sources) and specifies exactly how to send and render PDF citations so users get a complete, trustworthy experience.
