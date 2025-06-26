from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.pipeline import process_query

router = APIRouter()

class FullQueryRequest(BaseModel):
    query: str
    query_tag: str

@router.post("/full")
def run_full_pipeline(payload: FullQueryRequest):
    try:
        process_query(payload.query, payload.query_tag)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

