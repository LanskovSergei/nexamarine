import requests
import json
import time


def find_decision_makers_chunked(url: str, company_name: str, query: str) -> str:
    chunks = [
        f"На сайте компании {company_name} ({url}) найди информацию о директоре или CEO.",
        f"На сайте компании {company_name} ({url}) найди информацию об основателях или владельцах.",
        f"На сайте компании {company_name} ({url}) найди информацию о других ЛПР (менеджеры, руководители отделов и т.п.)."
    ]

    full_response = ""

    for i, chunk in enumerate(chunks):
        messages = [
            {"role": "system", "content": "Ты помощник по бизнес-анализу и ресерчу."},
            {"role": "user", "content": chunk + f" Запрос, по которому найдена компания: '{query}'"}
        ]

        try:
            response = requests.post("http://ollama:11434/api/chat", json={
                "model": "deepseek-v2.5",
                "messages": messages
            })
            lines = response.text.strip().splitlines()
            last_chunk = json.loads(lines[-1]) if len(lines) > 1 else response.json()
            content = last_chunk.get("message", {}).get("content", "").strip()
            full_response += f"\n\n# Ответ {i+1}:\n" + content
            time.sleep(1)  # на всякий случай пауза
        except Exception as e:
            print(f"❌ Ошибка запроса к DeepSeek (часть {i+1}):", e)
            full_response += f"\n\n# Ошибка в части {i+1}: {str(e)}"

    return full_response.strip()
