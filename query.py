from fastapi import APIRouter
from pydantic import BaseModel
from app.core.ollama_client import query_ollama

router = APIRouter()

class QueryRequest(BaseModel):
    prompt: str
    model: str = "mistral"
    system: str = "Ты — ассистент. Отвечай по делу." #заглушка

@router.post("/query")
def query_post(data: QueryRequest):
    result = query_ollama(
        prompt=data.prompt,
        model=data.model,
        system=data.system
    )
    return result
