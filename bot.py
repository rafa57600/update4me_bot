"""
Telegram Movie & Series Bot - Production Version
Main entry point with health check server for UptimeRobot
"""

import asyncio
import logging
import sys
import os
from threading import Thread

from flask import Flask
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from tmdb_client import tmdb

# Import handlers
from handlers import start, movies, series, trending, search, language, favorites, subscriptions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ============ Health Check Server for UptimeRobot ============

app = Flask(__name__)

@app.route('/')
def home():
    return "🎬 Movie Bot is running! 🚀"

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "running"}, 200

def run_flask():
    """Run Flask server in background thread"""
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ============ Bot Setup ============

async def on_startup():
    """Startup actions"""
    logger.info("🚀 Bot is starting...")
    logger.info("📡 Connected to TMDB API")
    logger.info("🌍 Multi-language support enabled")
    logger.info("⭐ Favorites system active")
    logger.info("🔔 Subscriptions system active")


async def on_shutdown():
    """Shutdown actions"""
    logger.info("🛑 Bot is shutting down...")
    await tmdb.close()
    logger.info("✅ Cleanup complete")


async def main():
    """Main function"""
    # Check if token is configured
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("❌ Error: Please configure your BOT_TOKEN")
        logger.error("   Set BOT_TOKEN environment variable on Render")
        return
    
    # Start Flask server in background for health checks
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 Health check server started")
    
    # Initialize bot with default properties
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Initialize dispatcher
    dp = Dispatcher()
    
    # Register routers (order matters!)
    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(favorites.router)
    dp.include_router(subscriptions.router)
    dp.include_router(movies.router)
    dp.include_router(series.router)
    dp.include_router(trending.router)
    dp.include_router(search.router)
    
    # Register startup/shutdown handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        # Delete webhook and start polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Bot started successfully!")
        logger.info("📱 Bot is now live on Telegram")
        
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise
