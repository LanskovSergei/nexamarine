# backend/app/core/serper_client.py
import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_serper(query: str):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
