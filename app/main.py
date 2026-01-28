from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from .models import SessionLocal, init_db, Article, Podcast
from .services.ingest import fetch_and_parse
from .services.digest import generate_podcast_script
from .services.audio import text_to_speech

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

class PodcastResponse(BaseModel):
    id: int
    title: str
    script: str
    audio_path: str

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
        status="processed" # Ready for digestion
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return new_article

@app.get("/articles", response_model=List[ArticleResponse])
def list_articles(db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.status != "archived").all()

@app.get("/podcasts", response_model=List[PodcastResponse])
def list_podcasts(db: Session = Depends(get_db)):
    return db.query(Podcast).order_by(Podcast.created_at.desc()).all()

@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return {"status": "deleted"}

@app.delete("/podcasts/{podcast_id}")
def delete_podcast(podcast_id: int, db: Session = Depends(get_db)):
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    # Optional: Delete actual file here
    db.delete(podcast)
    db.commit()
    return {"status": "deleted"}

@app.post("/generate", response_model=PodcastResponse)
async def generate_episode(db: Session = Depends(get_db)):
    # 1. Fetch unprocessed articles
    articles = db.query(Article).filter(Article.status == "processed").all()
    
    if not articles:
        raise HTTPException(status_code=400, detail="No new articles to process!")
        
    # 2. Prepare data for LLM
    article_data = [{"title": a.title, "content": a.content_clean} for a in articles]
    
    # 3. Generate Script (LLM)
    script = generate_podcast_script(article_data)
    
    # 4. Generate Audio (TTS)
    # Filename based on timestamp
    import time
    filename = f"podcast_{int(time.time())}.mp3"
    audio_path = await text_to_speech(script, filename)
    
    # 5. Save Podcast Record
    podcast = Podcast(
        title=f"ReadCast Daily Digest - {len(articles)} Articles",
        script=script,
        audio_path=audio_path
    )
    db.add(podcast)
    
    # 6. Mark articles as archived/done
    for a in articles:
        a.status = "archived"
        
    db.commit()
    db.refresh(podcast)
    
    return podcast
