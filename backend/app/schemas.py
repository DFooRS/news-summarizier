from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewsItemBase(BaseModel):
    title: str
    summary: str
    content: str
    source: str
    created_at: datetime
    image: Optional[str] = None
    url: Optional[str] = None

class NewsItem(NewsItemBase):
    id: int

    class Config:
        orm_mode = True