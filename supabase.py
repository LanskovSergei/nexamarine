import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_company(name: str, url: str, description: str = ""):
    try:
        data = {
            "name": name,
            "url": url,
            "description": description
        }

        # Проверка на дубликаты по URL
        existing = supabase.table("companies").select("id").eq("url", url).execute()
        if existing.data:
            return  # уже существует

        supabase.table("companies").insert(data).execute()
    except Exception as e:
        print(f"Ошибка сохранения компании: {e}")
