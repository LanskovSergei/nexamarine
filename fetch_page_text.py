import requests
from bs4 import BeautifulSoup

def fetch_page_text(url: str, timeout: int = 10) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Удаляем скрипты и стили
        for script_or_style in soup(["script", "style", "noscript"]):
            script_or_style.decompose()

        # Извлекаем видимый текст
        text = soup.get_text(separator="\n")
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        return text[:20000]  # ограничим до 20k символов, чтобы не уронить DeepSeek

    except Exception as e:
        print(f"❌ Ошибка при загрузке сайта {url}: {e}")
        return ""

# Пример
if __name__ == "__main__":
    url = "https://graintrade.co.za/"
    print(fetch_page_text(url))
