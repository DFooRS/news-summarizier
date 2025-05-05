from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import RawNews
from app import ProcessedNews

async def create_news_record(
    session: AsyncSession,
    content: str,
    source: str,
    url: str,
    summary: str
):
    raw_news = RawNews(
        content=content,
        content_hash=hashlib.md5(content.encode()).hexdigest(),
        source=source,
        url=url
    )
    session.add(raw_news)
    await session.commit()
    await session.refresh(raw_news)

    processed_news = ProcessedNews(
        raw_news_id=raw_news.id,
        summary=summary
    )
    session.add(processed_news)
    await session.commit()

    return raw_news