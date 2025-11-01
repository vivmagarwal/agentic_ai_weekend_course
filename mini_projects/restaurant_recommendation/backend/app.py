"""
Restaurant Recommendation System - FastAPI Backend
Serves frontend from root and provides search API endpoints
"""

import os
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import asyncio
import time
from tavily import AsyncTavilyClient
import google.generativeai as genai
import json

# Load environment from root .env
root_env = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(root_env)

# Initialize FastAPI app
app = FastAPI(title="Restaurant Recommendation System")

# Get API keys - using free tier APIs
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize API clients
tavily_client = AsyncTavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

# Initialize Gemini client (free tier)
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash-exp')
else:
    gemini_model = None


# Pydantic Models
class RestaurantQuery(BaseModel):
    query: str
    location: Optional[str] = None


class Restaurant(BaseModel):
    name: str
    address: str
    cuisine: str
    rating: Optional[str] = None
    description: str
    hours: Optional[str] = None
    price: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None


class SearchResponse(BaseModel):
    restaurants: List[Restaurant]
    source: str
    processing_time: float


# Search Functions
async def search_tavily(query: str, location: Optional[str]) -> List[Restaurant]:
    """Search restaurants using Tavily API"""
    if not tavily_client:
        raise HTTPException(status_code=500, detail="Missing TAVILY_API_KEY in environment")

    try:
        search_query = f"{query} restaurants in {location}" if location else f"{query} restaurants"
        response = await tavily_client.search(
            query=search_query,
            search_depth="advanced",
            max_results=10
        )

        restaurants = []
        for result in response.get("results", []):
            # Extract restaurant info from Tavily results
            restaurant = Restaurant(
                name=result.get("title", "Unknown Restaurant"),
                address=result.get("url", "Address not available"),
                cuisine=query,  # Use query as cuisine type
                rating=None,
                description=result.get("content", "No description available")[:200]
            )
            restaurants.append(restaurant)

        return restaurants
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tavily API Error: {str(e)}")


async def search_gemini(query: str, location: Optional[str]) -> List[Restaurant]:
    """Search restaurants using Google Gemini API (free tier)"""
    if not gemini_model:
        raise HTTPException(status_code=500, detail="Missing GOOGLE_API_KEY in environment")

    try:
        search_query = f"{query} restaurants in {location}" if location else f"{query} restaurants"

        prompt = f"""You are a restaurant recommendation expert. Find restaurants for: {search_query}

Return restaurant data in JSON format with an array of restaurants, each having these fields:
- name (string)
- address (string)
- cuisine (string)
- rating (string or null)
- description (string)
- hours (string or null)
- price (string or null)
- phone (string or null)
- website (string or null)

Return at least 3-5 restaurants if available. Return ONLY the JSON array, no other text."""

        # Call Gemini API (synchronous, wrap in async)
        response = await asyncio.to_thread(
            gemini_model.generate_content,
            prompt
        )

        # Parse LLM response
        content = response.text

        # Try to extract JSON from response
        try:
            # Look for JSON array in response
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end > start:
                json_str = content[start:end]
                data = json.loads(json_str)

                restaurants = []
                for item in data:
                    restaurant = Restaurant(
                        name=item.get("name", "Unknown Restaurant"),
                        address=item.get("address", "Address not available"),
                        cuisine=item.get("cuisine", query),
                        rating=item.get("rating"),
                        description=item.get("description", "No description available"),
                        hours=item.get("hours"),
                        price=item.get("price"),
                        phone=item.get("phone"),
                        website=item.get("website")
                    )
                    restaurants.append(restaurant)

                return restaurants
        except json.JSONDecodeError:
            pass

        # Fallback: create single restaurant from text response
        return [Restaurant(
            name="Restaurant suggestions",
            address="See description",
            cuisine=query,
            description=content[:500]
        )]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")


def merge_results(tavily_results: List[Restaurant], gemini_results: List[Restaurant]) -> List[Restaurant]:
    """Merge and deduplicate results from both sources"""
    merged = []
    seen_names = set()

    # Prefer Gemini results first (more structured)
    for restaurant in gemini_results:
        name_lower = restaurant.name.lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            merged.append(restaurant)

    # Add Tavily results if not duplicates
    for restaurant in tavily_results:
        name_lower = restaurant.name.lower()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            merged.append(restaurant)

    return merged


# API Endpoints
@app.get("/")
async def serve_frontend():
    """Serve frontend HTML"""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/search", response_model=SearchResponse)
async def search_restaurants(query: RestaurantQuery):
    """Search restaurants using Tavily and Google Gemini APIs (free tier)"""
    start_time = time.time()

    # Validate input
    if not query.query or len(query.query.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Please specify location and cuisine preference (e.g., 'italian food in Rome')"
        )

    try:
        # Search both APIs in parallel
        tavily_task = search_tavily(query.query, query.location)
        gemini_task = search_gemini(query.query, query.location)

        tavily_results, gemini_results = await asyncio.gather(
            tavily_task, gemini_task,
            return_exceptions=True
        )

        # Handle errors
        if isinstance(tavily_results, Exception):
            tavily_results = []
        if isinstance(gemini_results, Exception):
            gemini_results = []

        # Merge results
        merged_results = merge_results(
            tavily_results if isinstance(tavily_results, list) else [],
            gemini_results if isinstance(gemini_results, list) else []
        )

        if not merged_results:
            raise HTTPException(
                status_code=404,
                detail="No restaurants found for your query. Try different cuisine or location."
            )

        processing_time = time.time() - start_time

        return SearchResponse(
            restaurants=merged_results,
            source="merged",
            processing_time=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")


def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

if __name__ == "__main__":
    import uvicorn
    port = find_available_port(8000)
    print(f"🚀 Starting server on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
