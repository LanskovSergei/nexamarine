from fastapi import APIRouter, Request
from pydantic import BaseModel
import requests

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    model: str = "deepseek-coder"
    system: str = "You are a research assistant. Search the web and return structured facts."

@router.post("/search")
def search_post(data: SearchRequest):
    ollama_url = "http://ollama:11434/api/chat"
    messages = [
        {"role": "system", "content": data.system},
        {"role": "user", "content": f"Search the web and summarize: {data.query}"}
    ]
    
    try:
        response = requests.post(ollama_url, json={
            "model": data.model,
            "messages": messages
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
