from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.raw_news import RawNews
from app.models.processed_news import ProcessedNews
from app.schemas import NewsItem
from sqlalchemy.orm import joinedload

app = FastAPI(title="News Aggregator API")

# Настройка CORS для связи с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/news", response_model=List[NewsItem])
async def get_news_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RawNews)
        .options(joinedload(RawNews.processed_news))
        .order_by(RawNews.created_at.desc())
    )
    news = result.scalars().all()
    return [
        NewsItem(
            id=raw.id,
            title=raw.content[:50],  # Временное решение, замените на реальное поле title
            summary=raw.processed_news.summary,
            content=raw.content,
            source=raw.source,
            created_at=raw.created_at,
            url=raw.url,
            image=None  # Добавьте поле image, если оно есть
        )
        for raw in news
        if raw.processed_news
    ]

@app.get("/api/news/{news_id}", response_model=NewsItem)
async def get_news_detail(news_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RawNews)
        .options(joinedload(RawNews.processed_news))
        .filter(RawNews.id == news_id)
    )
    raw = result.scalars().first()
    if not raw or not raw.processed_news:
        raise HTTPException(status_code=404, detail="News not found")
    return NewsItem(
        id=raw.id,
        title=raw.content[:50],  # Временное решение, замените на реальное поле title
        summary=raw.processed_news.summary,
        content=raw.content,
        source=raw.source,
        created_at=raw.created_at,
        url=raw.url,
        image=None  # Добавьте поле image, если оно есть
    )