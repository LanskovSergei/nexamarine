from fastapi import APIRouter
from pydantic import BaseModel
import requests
from app.core.serper_client import search_serper  # Импортируем клиент Serper

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    model: str = "deepseek-coder"  # Можно указать "serper" или "deepseek-coder"
    system: str = "You are a research assistant. Search the web and return structured facts."

@router.post("/search")
def search_post(data: SearchRequest):
    if data.model == "serper":
        try:
            result = search_serper(data.query)
            return result
        except Exception as e:
            return {"error": str(e)}

    # Обработка через Ollama
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

        # Если Ollama возвращает много JSON строк (streaming), берём последнюю
        lines = response.text.strip().splitlines()
        last_line = lines[-1]
        return response.json() if len(lines) == 1 else requests.utils.json.loads(last_line)

    except Exception as e:
        return {"error": str(e)}


