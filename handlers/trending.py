"""
Trending Handler - Display trending movies and series - Localized
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tmdb_client import tmdb
from keyboards.inline import get_trending_keyboard, get_back_keyboard
from translations import get_text, get_tmdb_language
from user_prefs import get_user_language

router = Router()


@router.message(Command("trending"))
async def cmd_trending(message: Message):
    """Handle /trending command"""
    user_lang = get_user_language(message.from_user.id)
    await show_trending(message, page=1, lang=user_lang)


@router.callback_query(F.data.startswith("trending:"))
async def callback_trending(callback: CallbackQuery):
    """Handle trending pagination"""
    page = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_trending(callback.message, page=page, edit=True, lang=user_lang)
    await callback.answer()


async def show_trending(message: Message, page: int = 1, edit: bool = False, lang: str = "en"):
    """Show trending content (movies and series)"""
    tmdb_lang = get_tmdb_language(lang)
    data = await tmdb.get_trending(media_type="all", time_window="week", page=page, language=tmdb_lang)
    results = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 50)  # Cap at 50 pages
    
    if not results:
        text = get_text(lang, "no_results")
        keyboard = get_back_keyboard(lang)
    else:
        item = results[0]
        media_type = item.get("media_type", "movie")
        
        # Format based on type
        if media_type == "movie":
            formatted = tmdb.format_movie(item, lang)
            emoji = "🎬"
        else:
            formatted = tmdb.format_series(item, lang)
            emoji = "📺"
        
        text = f"{get_text(lang, 'trending_week')}\n\n{emoji} {formatted}"
        keyboard = get_trending_keyboard(
            page=page,
            total_pages=total_pages,
            item_id=item.get("id"),
            media_type=media_type,
            lang=lang
        )
    
    if edit:
        try:
            poster_url = tmdb.get_poster_url(results[0].get("poster_path")) if results else None
            if poster_url:
                await message.delete()
                await message.answer_photo(
                    photo=poster_url,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            else:
                await message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except Exception:
            try:
                await message.delete()
            except:
                pass
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        poster_url = tmdb.get_poster_url(results[0].get("poster_path")) if results else None
        if poster_url:
            await message.answer_photo(
                photo=poster_url,
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
