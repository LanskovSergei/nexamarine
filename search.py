from fastapi import APIRouter
from pydantic import BaseModel
import requests
from app.core.serper_client import search_serper  # Импортируем клиент Serper
from app.db.supabase import save_company  # Импортируем функцию сохранения

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    model: str = "deepseek-coder"  # "serper" или название модели Ollama
    system: str = "You are a research assistant. Search the web and return structured facts."

@router.post("/search")
def search_post(data: SearchRequest):
    if data.model == "serper":
        try:
            result = search_serper(data.query)

            # Сохраняем найденные компании в Supabase
            for item in result.get("organic", []):
                title = item.get("title")
                link = item.get("link")
                snippet = item.get("snippet", "")
                if title and link:
                    save_company(title, link, snippet)

            return result
        except Exception as e:
            return {"error": str(e)}

    # Обработка через Ollama
    ollama_url = "http://ollama:11434/api/chat"
    messages = [
        {"role": "system", "content": data.system},



