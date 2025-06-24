from fastapi import FastAPI
from app.api import query
from app.api import search

app = FastAPI()

app.include_router(query.router, tags=["query"])
app.include_router(search.router, tags=["search"])
