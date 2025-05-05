# config.py
import os
from dotenv import load_dotenv

load_dotenv(".env")

DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME")
}

# Telegram API
API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
SESSION_NAME = os.getenv("TG_SESSION_NAME", "news_parser_session")

# Parsing settings
CHANNELS_TO_PARSE = os.getenv("TG_CHANNELS").split(",") if os.getenv("TG_CHANNELS") else []
MAX_POSTS_PER_CHANNEL = int(os.getenv("MAX_POSTS_PER_CHANNEL", 100))