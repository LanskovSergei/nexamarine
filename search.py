# backend/app/api/search.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.serper_client import search_serper

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.post("/search")
def search_post(data: SearchRequest):
    try:
        results = search_serper(data.query)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


