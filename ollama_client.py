# backend/app/core/ollama_client.py

import requests
import json

def run_model(model: str, prompt: str) -> str:
    messages = [
        {"role": "system", "content": "Ты — ассистент по поиску B2B компаний."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = requests.post("http://ollama:11434/api/chat", json={
            "model": model,
            "messages": messages
        })

        print("[Ollama DEBUG] Status Code:", response.status_code)
        print("[Ollama DEBUG] Full Response Text:", response.text)

        # Попробовать распарсить сразу
        try:
            data = response.json()
            if "message" in data:
                return data["message"]["content"].strip()
        except Exception as e:
            print("[Ollama ERROR] JSON parse failed:", e)

        # Если стрим, то вытаскиваем последнее сообщение
        chunks = response.text.strip().splitlines()
        if not chunks:
            return ""

        last_chunk = json.loads(chunks[-1])
        return last_chunk.get("message", {}).get("content", "").strip()

    except Exception as e:
        print("❌ Ollama error:", e)
        return ""


