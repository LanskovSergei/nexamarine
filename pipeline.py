# 📁 backend/app/core/pipeline.py

from core.serper import search_companies
from core.deepseek import find_contacts_for_site
from db.supabase import save_company_with_score, save_contacts_for_company, supabase
from typing import List

def company_exists(url: str) -> bool:
    try:
        response = supabase.table("companies").select("url").eq("url", url).execute()
        return len(response.data) > 0
    except Exception as e:
        print("Error checking company existence:", e)
        return False

def process_query(query: str):
    print(f"🔍 Processing query: {query}")
    companies: List[dict] = search_companies(query)

    for company in companies:
        url = company.get("url")
        if not url:
            print("⛔ Пропущена компания без URL")
            continue

        if company_exists(url):
            print(f"⚠️ Компания уже существует в базе: {url}")
            continue

        print(f"💾 Сохраняем компанию: {company.get('name')}")
        save_company_with_score({
            "name": company.get("title"),
            "url": url,
            "description": company.get("snippet"),
            "ai_score": None  # пока не используем
        })

        print(f"🧠 Ищем контакты через DeepSeek для {url}...")
        contacts = find_contacts_for_site(url)
        if contacts:
            save_contacts_for_company(url, contacts)
        else:
            print("🙈 Контакты не найдены.")
