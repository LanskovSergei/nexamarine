import json
import requests

def query_ollama(prompt: str, model: str = "mistral", system: str = "You are a helpful assistant."):
    response = requests.post("http://ollama:11434/api/chat", json={
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    })
    response.raise_for_status()

    # Потоковый вывод, берём последнюю строку
    lines = response.text.strip().splitlines()
    last_line = lines[-1]
    
    print(">>> DEBUG last_line:", last_line)

    data = json.loads(last_line)

    if not data.get("message", {}).get("content"):
        return {"warning": "Модель не вернула текст", "raw": data}

    return data
