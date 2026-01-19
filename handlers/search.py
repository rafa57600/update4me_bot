"""
Search Handler - Search for movies and series
Supports both command and inline mode
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.filters import Command
from hashlib import md5

from tmdb_client import tmdb
from keyboards.inline import get_search_results_keyboard, get_back_keyboard

router = Router()


@router.message(Command("search"))
async def cmd_search(message: Message):
    """Handle /search command"""
    # Extract search query from command
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.answer(
            "🔍 <b>How to search:</b>\n\n"
            "1️⃣ Use command: <code>/search Movie Name</code>\n\n"
            "2️⃣ Or use inline mode:\n"
            "Type <code>@YourBotName query</code> in any chat",
            parse_mode="HTML",
            reply_markup=get_back_keyboard()
        )
        return
    
    query = args[1].strip()
    await show_search_results(message, query, page=1)


@router.callback_query(F.data.startswith("search:"))
async def callback_search(callback: CallbackQuery):
    """Handle search pagination"""
    parts = callback.data.split(":")
    query = parts[1]
    page = int(parts[2]) if len(parts) > 2 else 1
    await show_search_results(callback.message, query, page=page, edit=True)
    await callback.answer()


async def show_search_results(message: Message, query: str, page: int = 1, edit: bool = False):
    """Show search results"""
    data = await tmdb.search_multi(query=query, page=page)
    results = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 50)
    
    # Filter to only movies and TV shows
    results = [r for r in results if r.get("media_type") in ["movie", "tv"]]
    
    if not results:
        text = f"🔍 <b>Search:</b> {query}\n\n❌ No results found."
        keyboard = get_back_keyboard()
    else:
        item = results[0]
        media_type = item.get("media_type", "movie")
        
        if media_type == "movie":
            formatted = tmdb.format_movie(item)
            emoji = "🎬"
        else:
            formatted = tmdb.format_series(item)
            emoji = "📺"
        
        text = f"🔍 <b>Search:</b> {query}\n\n{emoji} {formatted}"
        keyboard = get_search_results_keyboard(
            page=page,
            total_pages=total_pages,
            query=query,
            item_id=item.get("id"),
            media_type=media_type
        )
    
    if edit:
        try:
            await message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except Exception:
            await message.delete()
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.inline_query()
async def inline_search(inline_query: InlineQuery):
    """Handle inline search queries"""
    query = inline_query.query.strip()
    
    if not query:
        # Show hint when no query
        results = [
            InlineQueryResultArticle(
                id="hint",
                title="🔍 Type to search...",
                description="Search for movies and TV series",
                input_message_content=InputTextMessageContent(
                    message_text="Use: @BotName <movie or series name>"
                )
            )
        ]
        await inline_query.answer(results, cache_time=1)
        return
    
    # Search TMDB
    data = await tmdb.search_multi(query=query, page=1)
    search_results = data.get("results", [])[:10]  # Limit to 10 results
    
    # Filter to only movies and TV shows
    search_results = [r for r in search_results if r.get("media_type") in ["movie", "tv"]]
    
    results = []
    for item in search_results:
        media_type = item.get("media_type", "movie")
        
        if media_type == "movie":
            title = item.get("title", "Unknown")
            year = item.get("release_date", "")[:4] if item.get("release_date") else ""
            emoji = "🎬"
            formatted = tmdb.format_movie(item)
        else:
            title = item.get("name", "Unknown")
            year = item.get("first_air_date", "")[:4] if item.get("first_air_date") else ""
            emoji = "📺"
            formatted = tmdb.format_series(item)
        
        rating = item.get("vote_average", 0)
        overview = item.get("overview", "No description")[:100]
        
        # Create unique ID
        result_id = md5(f"{media_type}_{item.get('id')}".encode()).hexdigest()
        
        results.append(
            InlineQueryResultArticle(
                id=result_id,
                title=f"{emoji} {title} ({year})",
                description=f"⭐ {rating:.1f} | {overview}...",
                thumbnail_url=tmdb.get_poster_url(item.get("poster_path")),
                input_message_content=InputTextMessageContent(
                    message_text=formatted,
                    parse_mode="HTML"
                )
            )
        )
    
    if not results:
        results = [
            InlineQueryResultArticle(
                id="no_results",
                title="❌ No results found",
                description=f"No movies or series match '{query}'",
                input_message_content=InputTextMessageContent(
                    message_text=f"❌ No results found for: {query}"
                )
            )
        ]
    
    await inline_query.answer(results, cache_time=60)
