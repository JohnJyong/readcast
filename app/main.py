from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from .models import SessionLocal, init_db, Article
from .services.ingest import fetch_and_parse

app = FastAPI(title="ReadCast API", version="0.1.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DTOs
class URLRequest(BaseModel):
    url: str
    source: str = "web"

class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    status: str

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to ReadCast API 🎙️"}

@app.post("/ingest", response_model=ArticleResponse)
def ingest_article(request: URLRequest, db: Session = Depends(get_db)):
    # 1. Check if exists
    existing = db.query(Article).filter(Article.url == request.url).first()
    if existing:
        return existing

    # 2. Fetch Content (Async in prod, Sync for MVP)
    data = fetch_and_parse(request.url)
    
    if data["status"] == "error":
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {data['content']}")

    # 3. Save to DB
    new_article = Article(
        url=request.url,
        title=data["title"],
        content_clean=data["content"],
        source=request.source,
        status="processed"
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return new_article

@app.get("/articles", response_model=List[ArticleResponse])
def list_articles(db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.status != "archived").all()
