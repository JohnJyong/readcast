from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./readcast.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String, nullable=True)
    content_raw = Column(Text, nullable=True)  # HTML or scraped text
    content_clean = Column(Text, nullable=True) # Markdown/Clean text
    source = Column(String, default="web") # wechat, twitter, web
    status = Column(String, default="pending") # pending, processed, archived
    created_at = Column(DateTime, default=datetime.utcnow)

class Podcast(Base):
    __tablename__ = "podcasts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    audio_path = Column(String)
    transcript = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
