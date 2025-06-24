import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY", "a039b5e1bba82d68b0557cdc3169afca8d2a6bf9")
SERPER_URL = "https://google.serper.dev/search"

def search_serper(query: str):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }

    response = requests.post(SERPER_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
