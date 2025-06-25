from fastapi import APIRouter
from pydantic import BaseModel
import requests
import json

from app.core.serper_client import search_serper
from app.db.supabase import save_company_with_score, update_company_contacts
from app.core.lpr_finder import find_lpr_with_ollama

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    model: str = "mistral"
    system: str = "You are a research assistant. Search the web and return structured facts."


@router.post("/search")
def search_post(data: SearchRequest):
    if data.model == "serper":
        try:
            result = search_serper(data.query)
            companies = result.get("organic", [])

            for company in companies:
                name = company.get("title")
                url = company.get("link")
                description = company.get("snippet")

                prompt = f"Ты аналитик. Оцени по шкале от 0 до 100, насколько компания '{name}' подходит под запрос '{data.query}'. Напиши только число."
                ollama_url = "http://ollama:11434/api/chat"
                messages = [
                    {"role": "system", "content": "You are a research assistant."},
                    {"role": "user", "content": prompt}
                ]

                try:
                    response = requests.post(ollama_url, json={
                        "model": "mistral",
                        "messages": messages
                    })
                    lines = response.text.strip().splitlines()
                    last = json.loads(lines[-1]) if len(lines) > 1 else response.json()
                    score = last.get("message", {}).get("content", "").strip()
                except Exception as e:
                    print("Error scoring:", e)
                    score = ""

                # Сохраняем компанию
                save_company_with_score({
                    "name": name,
                    "url": url,
                    "description": description,
                    "ai_score": score
                })

                # Ищем ЛПР
                try:
                    lpr_data = find_lpr_with_ollama(url, name, data.query)
                    update_company_contacts(url, lpr_data)
                except Exception as e:
                    print("LPR error:", e)

            return {"status": "ok", "companies_processed": len(companies)}

        except Exception as e:
            return {"error": str(e)}

    # Если модель не serper, просто обращаемся к Ollama
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
        lines = response.text.strip().splitlines()
        return response.json() if len(lines) == 1 else json.loads(lines[-1])
    except Exception as e:
        return {"error": str(e)}





