import requests

def query_ollama(prompt: str, model: str = "mistral", system: str = ""):
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False
    }
    response = requests.post("http://ollama:11434/api/generate", json=payload)
    response.raise_for_status()
    return response.json()
