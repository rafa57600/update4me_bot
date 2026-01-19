"""
Series Handler - Display latest and popular TV series - Localized
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tmdb_client import tmdb
from keyboards.inline import get_series_keyboard, get_popular_series_keyboard, get_back_keyboard
from translations import get_text, get_tmdb_language
from user_prefs import get_user_language

router = Router()


@router.message(Command("series"))
async def cmd_series(message: Message):
    """Handle /series command"""
    user_lang = get_user_language(message.from_user.id)
    await show_series(message, page=1, lang=user_lang)


@router.callback_query(F.data.startswith("series:"))
async def callback_series(callback: CallbackQuery):
    """Handle series pagination"""
    page = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_series(callback.message, page=page, edit=True, lang=user_lang)
    await callback.answer()


@router.callback_query(F.data.startswith("popular_series:"))
async def callback_popular_series(callback: CallbackQuery):
    """Handle popular series pagination"""
    page = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_popular_series(callback.message, page=page, edit=True, lang=user_lang)
    await callback.answer()


@router.callback_query(F.data.startswith("details_series:"))
async def callback_series_details(callback: CallbackQuery):
    """Handle series details"""
    series_id = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_series_details(callback.message, series_id, edit=True, lang=user_lang)
    await callback.answer()


@router.callback_query(F.data.startswith("trailer_series:"))
async def callback_series_trailer(callback: CallbackQuery):
    """Handle series trailer request"""
    series_id = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    tmdb_lang = get_tmdb_language(user_lang)
    
    videos = await tmdb.get_series_videos(series_id, language=tmdb_lang)
    results = videos.get("results", [])
    
    # Find YouTube trailer
    trailer = None
    for video in results:
        if video.get("site") == "YouTube" and video.get("type") in ["Trailer", "Teaser"]:
            trailer = video
            break
    
    # If no trailer in user language, try English
    if not trailer:
        videos = await tmdb.get_series_videos(series_id, language="en-US")
        results = videos.get("results", [])
        for video in results:
            if video.get("site") == "YouTube" and video.get("type") in ["Trailer", "Teaser"]:
                trailer = video
                break
    
    if trailer:
        youtube_url = f"https://www.youtube.com/watch?v={trailer['key']}"
        await callback.answer(get_text(user_lang, "opening_trailer"), show_alert=False)
        await callback.message.answer(f"📺 <b>Trailer</b>\n\n{youtube_url}", parse_mode="HTML")
    else:
        await callback.answer(get_text(user_lang, "no_trailer"), show_alert=True)


async def show_series(message: Message, page: int = 1, edit: bool = False, lang: str = "en"):
    """Show latest series (airing today)"""
    tmdb_lang = get_tmdb_language(lang)
    data = await tmdb.get_latest_series(page=page, language=tmdb_lang)
    results = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 50)  # Cap at 50 pages
    
    if not results:
        text = get_text(lang, "no_series")
        keyboard = get_back_keyboard(lang)
    else:
        series = results[0]
        text = f"{get_text(lang, 'airing_today')}\n\n{tmdb.format_series(series, lang)}"
        keyboard = get_series_keyboard(
            page=page,
            total_pages=total_pages,
            series_id=series.get("id"),
            has_trailer=True,
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


async def show_popular_series(message: Message, page: int = 1, edit: bool = False, lang: str = "en"):
    """Show popular TV series"""
    tmdb_lang = get_tmdb_language(lang)
    data = await tmdb.get_popular_series(page=page, language=tmdb_lang)
    results = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 50)
    
    if not results:
        text = get_text(lang, "no_series")
        keyboard = get_back_keyboard(lang)
    else:
        series = results[0]
        text = f"{get_text(lang, 'popular_series_title')}\n\n{tmdb.format_series(series, lang)}"
        keyboard = get_popular_series_keyboard(
            page=page,
            total_pages=total_pages,
            series_id=series.get("id"),
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


async def show_series_details(message: Message, series_id: int, edit: bool = False, lang: str = "en"):
    """Show detailed series information"""
    tmdb_lang = get_tmdb_language(lang)
    series = await tmdb.get_series_details(series_id, language=tmdb_lang)
    
    if "error" in series or not series.get("name"):
        text = get_text(lang, "no_series")
        keyboard = get_back_keyboard(lang)
    else:
        title = series.get("name", "Unknown")
        rating = series.get("vote_average", 0)
        first_air = series.get("first_air_date", "N/A")
        seasons = series.get("number_of_seasons", 0)
        episodes = series.get("number_of_episodes", 0)
        status = series.get("status", "Unknown")
        genres = ", ".join([g["name"] for g in series.get("genres", [])[:3]])
        overview = series.get("overview", "No description available.")
        
        text = (
            f"📺 <b>{title}</b>\n\n"
            f"{get_text(lang, 'rating')}: {rating:.1f}/10\n"
            f"{get_text(lang, 'first_aired')}: {first_air}\n"
            f"{get_text(lang, 'seasons')}: {seasons} | {get_text(lang, 'episodes')}: {episodes}\n"
            f"{get_text(lang, 'status')}: {status}\n"
            f"{get_text(lang, 'genres')}: {genres}\n\n"
            f"{get_text(lang, 'overview')}\n{overview}"
        )
        keyboard = get_back_keyboard(lang)
    
    if edit:
        # Always delete and send new message to avoid photo/text conflicts
        try:
            await message.delete()
        except Exception:
            pass
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
