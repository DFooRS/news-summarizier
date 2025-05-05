from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ProcessedNews(Base):
    __tablename__ = 'processed_news'

    id = Column(Integer, primary_key=True, index=True)
    raw_news_id = Column(
        Integer,
        ForeignKey('raw_news.id'),
        unique=True, 
        nullable=False,
        index=True
    )
    summary = Column(Text, nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default='now()')

    # Обратная ссылка
    raw_news = relationship("RawNews", back_populates="processed_news")

    def __repr__(self):
        return f"<ProcessedNews(id={self.id}, raw_news_id={self.raw_news_id})>"