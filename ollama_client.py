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

    # Пробуем распарсить только последнюю строку (если это потоковый вывод)
    lines = response.text.strip().splitlines()
    last_line = lines[-1]
    return json.loads(last_line)
