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
    return response.json()
vvvvvvvvvvvvvvvv
