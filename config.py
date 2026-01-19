"""
Configuration for Telegram Movie Bot

Instructions:
1. Get Telegram Bot Token from @BotFather (https://t.me/botfather)
2. Get TMDB API Key from https://www.themoviedb.org/settings/api
3. Replace the placeholder values below with your actual keys
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Telegram Bot Token - Get from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")

# TMDB API Key - Get from themoviedb.org
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY_HERE")

# TMDB API Base URL
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Items per page
ITEMS_PER_PAGE = 5
