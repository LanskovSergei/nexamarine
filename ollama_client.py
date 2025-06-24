import json
import requests

def query_ollama(prompt: str, model: str = "mistral", system: str = "Ты — ассистент. Отвечай по делу."):
    response = requests.post("http://ollama:11434/api/chat", json={
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    })
    response.raise_for_status()

    # Парсим последнюю строку
    lines = response.text.strip().splitlines()
    return json.loads(lines[-1])

def search_ollama(query: str, model: str = "deepseek-coder", system: str = "You are a research assistant. Search the internet and return useful sources."):
    response = requests.post("http://ollama:11434/api/chat", json={
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": query}
        ]
    })
    response.raise_for_status()

    # Здесь тоже стрим — берём последнюю строку
    lines = response.text.strip().splitlines()
    return json.loads(lines[-1])

