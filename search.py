# backend/app/api/search.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.ollama_client import run_model
from app.core.serper_client import search_serper
from app.db.supabase import save_company_with_score, save_contact_with_company

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    model: str = "mistral"

@router.post("/search")
async def search(request: SearchRequest):
    query = request.query
    model = request.model

    print("🔍 Search query:", query)

    # Step 1: Run search via Serper
    serper_results = search_serper(query)
    print("🔗 Serper results:", serper_results)

    urls = [r["link"] for r in serper_results.get("organic", []) if "link" in r]
    print("🔗 Extracted URLs:", urls)

    if not urls:
        print("⚠️ No URLs found from Serper")
        return {"message": "No links found in search results."}

    # Step 2: Format prompt for the model
    prompt = f"""
You are an AI assistant helping to identify B2B companies and their key decision makers.

From the following list of company URLs:
{chr(10).join(urls)}

Return a list of companies with:
- Company name
- Website
- Country (if available)
- At least 1–3 key decision makers (Name, Role, Email if public)
- Relevance score from 1 to 10 (confidence that the company is a match)

Respond only in JSON format as a list of objects like:
[
  {{
    "name": "Company A",
    "url": "https://a.com",
    "country": "USA",
    "score": 9.2,
    "contacts": [
      {{
        "name": "John",
        "role": "CEO",
        "email": "john@a.com"
      }}
    ]
  }},
  ...
]
    """.strip()

    print("🧠 Prompt sent to model:", prompt[:500], "...\n")  # Trimmed

    result = run_model(model=model, prompt=prompt)
    print("🤖 Raw model result:", result)

    try:
        companies = eval(result)
        print("✅ Parsed companies:", companies)
    except Exception as e:
        print("❌ Failed to parse model output:", str(e))
        return {"error": "Could not parse model output."}

    for company in companies:
        print("💾 Saving company:", company)
        save_company_with_score(company, company.get("score", 0))

        for contact in company.get("contacts", []):
            print(f"👤 Saving contact {contact.get('name')} to {company.get('url')}")
            save_contact_with_company(contact, company.get("url"))

    return {"message": "Search completed", "companies_saved": len(companies)}






