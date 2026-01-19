# 🎬 Telegram Movie & Series Bot

A feature-rich Telegram bot that shows latest movies, series, and trending content using TMDB API.

## ✨ Features

- 🎬 **Latest Movies** - Now playing in theaters
- 📺 **Latest Series** - TV shows airing today
- 🔥 **Trending** - What's popular this week
- 🔍 **Search** - Find any movie or series (+ inline mode)
- ⭐ **Favorites** - Save your favorite movies/series
- 🔔 **Subscriptions** - Subscribe to genres and topics
- 🌍 **Multi-language** - 15 languages supported
- 🖼️ **Posters** - Beautiful movie/series images
- 📖 **Details** - Full info with ratings, genres, overview

## 🚀 Deployment on Render

### 1. Fork/Clone to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/movie-bot.git
git push -u origin main
```

### 2. Create Render Web Service

1. Go to [render.com](https://render.com) and sign up
2. Click **New** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `movie-bot` (or your choice)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

### 3. Add Environment Variables

In Render dashboard, add these environment variables:

| Variable | Value |
|----------|-------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather |
| `TMDB_API_KEY` | Your TMDB API key from themoviedb.org |

### 4. Setup UptimeRobot (Keep Bot Running)

Render's free tier sleeps after 15 min of inactivity. Use UptimeRobot to keep it awake:

1. Go to [uptimerobot.com](https://uptimerobot.com) and sign up
2. Click **Add New Monitor**
3. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Movie Bot
   - **URL**: `https://your-app-name.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
4. Click **Create Monitor**

## 🔧 Local Development

### Setup

1. Clone the repository
2. Create `.env` file:
```env
BOT_TOKEN=your_telegram_bot_token
TMDB_API_KEY=your_tmdb_api_key
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the bot:
```bash
python bot.py
```

## 📝 Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu |
| `/movies` | Latest movies |
| `/series` | Latest series |
| `/trending` | Trending this week |
| `/search <query>` | Search movies/series |
| `/favorites` | Your saved favorites |
| `/subscriptions` | Manage subscriptions |
| `/language` | Change language |

## 🌍 Supported Languages

🇬🇧 English, 🇫🇷 Français, 🇪🇸 Español, 🇩🇪 Deutsch, 🇮🇹 Italiano, 🇵🇹 Português, 🇸🇦 العربية, 🇯🇵 日本語, 🇰🇷 한국어, 🇨🇳 中文, 🇷🇺 Русский, 🇹🇷 Türkçe, 🇮🇳 हिन्दी, 🇳🇱 Nederlands, 🇵🇱 Polski

## 📁 Project Structure

```
├── bot.py              # Main entry point + health server
├── config.py           # Configuration
├── tmdb_client.py      # TMDB API client
├── translations.py     # Multi-language support
├── user_prefs.py       # User preferences storage
├── handlers/           # Command handlers
│   ├── start.py
│   ├── movies.py
│   ├── series.py
│   ├── trending.py
│   ├── search.py
│   ├── language.py
│   ├── favorites.py
│   └── subscriptions.py
├── keyboards/          # Inline keyboard builders
│   └── inline.py
├── requirements.txt    # Dependencies
├── Procfile           # Render process file
└── runtime.txt        # Python version
```

## 📄 License

MIT - Free to use and modify!
