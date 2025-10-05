# Restaurant Recommendation System

A chat-based restaurant recommendation system that accepts natural language queries and provides real-time restaurant recommendations using Tavily and Perplexity search APIs.

## Features
- Natural language restaurant search
- Real-time web search via Tavily and Perplexity APIs
- Chat-style interface with loading states
- Comprehensive restaurant information display
- Mobile-responsive design

## Setup

### Prerequisites
- Python 3.9+
- API keys for Tavily and Perplexity (configured in root .env)

### Installation

```bash
# Navigate to backend directory
cd mini_projects/002_restaurant_recommendation/backend

# Create virtual environment
uv venv
source .venv/bin/activate  # Unix/MacOS
# or: .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Configuration

Ensure the root `.env` file at `/Users/vivmagarwal/Work/opensource/agentic_ai_course_uwc/.env` contains:
```
TAVILY_API_KEY=your_tavily_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here
```

## Usage

### Run the application
```bash
cd backend
uvicorn app:app --reload --port 8000
```

Or:
```bash
python app.py
```

### Access the application
Open http://localhost:8000 in your browser

### Example queries
- "indian veg food in bangalore"
- "italian restaurants near downtown"
- "chinese food in san francisco"

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: HTML + Tailwind CSS + JavaScript
- **Search APIs**: Tavily, Perplexity
- **Deployment**: Single port (8000)

## API Endpoints
- `GET /` - Serves frontend chat UI
- `POST /api/search` - Search restaurants by natural language query
- `GET /api/health` - Health check

## Development Status
🚧 Under development - Alpha version
