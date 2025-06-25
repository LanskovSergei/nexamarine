import requests
import json

def find_lpr_with_ollama(url: str, company_name: str, query: str) -> str:
    prompt = (
        f"На сайте компании {company_name} ({url}) найди информацию о людях, "
        f"которые могут быть лицами, принимающими решения (ЛПР), "
        f"например директор, CEO, менеджер, основатель и т.п. "
        f"Запрос, по которому компания найдена: '{query}'. "
        f"Верни список ЛПР с именами, должностями и, если есть, контактами."
    )

    messages = [
        {"role": "system", "content": "Ты помощник по бизнес-анализу и ресерчу."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = requests.post("http://ollama:11434/api/chat", json={
            "model": "deepseek-v2.5",
            "messages": messages
        })
        chunks = response.text.strip().splitlines()
        last_chunk = json.loads(chunks[-1]) if len(chunks) > 1 else response.json()
        return last_chunk.get("message", {}).get("content", "").strip()
    except Exception as e:
        print("LPR search failed:", e)
        return ""
