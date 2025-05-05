import asyncio
from services.telegram_parser import TelegramParser


if __name__ == "__main__":
    parser = TelegramParser()
    asyncio.run(parser.run())