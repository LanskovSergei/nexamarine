from fastapi import APIRouter, Request
from app.core.search_agent import search_and_analyze

router = APIRouter()

@router.post("/search")
def search_post(request: Request):
    data = request.json()
    query = data.get("query")
    if not query:
        return {"error": "Query is required"}
    return search_and_analyze(query)
