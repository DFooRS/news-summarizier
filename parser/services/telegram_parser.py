import asyncio
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

from telethon.sync import TelegramClient
from telethon.tl.types import Message
from sqlalchemy.orm import Session

from config import (
    API_ID,
    API_HASH,
    SESSION_NAME,
    CHANNELS_TO_PARSE,
    MAX_POSTS_PER_CHANNEL
)

from models import NewsItem, engine

class TelegramParser:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    async def _get_existing_hashes(self) -> set:
        """Получить хеши уже сохраненных новостей"""
        with Session(engine) as session:
            return {item.content_hash for item in session.query(NewsItem.content_hash).all()}

    @staticmethod
    def _generate_content_hash(text: str) -> str:
        """Генерация MD5 хеша контента для проверки дублей"""
        return hashlib.md5(text.encode()).hexdigest()

    def _format_message(self, message: Message, channel: str) -> Optional[Dict]:
        """Форматирование сообщения в структуру новости"""
        if not message.text:
            return None

        text = message.text.strip()
        if not text or len(text) < 50:  # Фильтр коротких сообщений
            return None

        return {
            'content': text,
            'content_hash': self._generate_content_hash(text),
            'source': f"t.me/{channel}",
            'date': message.date,
            'url': f"https://t.me/{channel}/{message.id}",
            'raw_data': str(message.to_dict())  # Для дебага
        }

    async def parse_channel(self, channel: str, limit: int = MAX_POSTS_PER_CHANNEL) -> List[Dict]:
        try:
            messages = []
            async for message in self.client.iter_messages(channel, limit=limit):
                if formatted := self._format_message(message, channel):
                    messages.append(formatted)
            return messages
        except Exception as e:
            print(f"Ошибка парсинга {channel}: {str(e)}")
            return []

    async def filter_new_posts(self, posts: List[Dict]) -> List[Dict]:"
        existing_hashes = await self._get_existing_hashes()
        return [p for p in posts if p['content_hash'] not in existing_hashes]

    async def save_to_db(self, posts: List[Dict]):
        with Session(engine) as session:
            for post in posts:
                news_item = NewsItem(
                    content=post['content'],
                    content_hash=post['content_hash'],
                    source=post['source'],
                    url=post['url'],
                    published_at=post['date'],
                    is_processed=False,
                    created_at=datetime.utcnow()
                )
                session.add(news_item)
            session.commit()

    async def run(self):
        async with self.client:
            for channel in CHANNELS_TO_PARSE:
                print(f"Парсинг канала {channel}...")
                posts = await self.parse_channel(channel)
                new_posts = await self.filter_new_posts(posts)

                if new_posts:
                    await self.save_to_db(new_posts)
                    print(f"Добавлено {len(new_posts)} новых постов из {channel}")
                else:
                    print(f"Новых постов в {channel} не найдено")


if __name__ == "__main__":
    parser = TelegramParser()

    try:
        asyncio.run(parser.run())
    except KeyboardInterrupt:
        print("Парсинг остановлен пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")