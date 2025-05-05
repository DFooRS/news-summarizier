from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class RawNews(Base):
    __tablename__ = 'raw_news'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String(32), unique=True, index=True)
    source = Column(String(100))
    url = Column(String(255), unique=True)
    created_at = Column(DateTime(timezone=True), server_default='now()')

    processed_news = relationship(
        "ProcessedNews",
        back_populates="raw_news",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<RawNews(id={self.id}, source={self.source[:20]}...)>"