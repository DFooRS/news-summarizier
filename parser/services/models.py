from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import DB_CONFIG

Base = declarative_base()

class NewsItem(Base):
    __tablename__ = 'raw_news'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String(32), unique=True)
    source = Column(String(100))
    url = Column(String(255), unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG.get('port', '5432')}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)