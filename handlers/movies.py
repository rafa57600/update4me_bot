"""
Movies Handler - Display latest and popular movies - Localized
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from tmdb_client import tmdb
from keyboards.inline import get_movies_keyboard, get_popular_movies_keyboard, get_back_keyboard
from translations import get_text, get_tmdb_language
from user_prefs import get_user_language

router = Router()


@router.message(Command("movies"))
async def cmd_movies(message: Message):
    """Handle /movies command"""
    user_lang = get_user_language(message.from_user.id)
    await show_movies(message, page=1, lang=user_lang)


@router.callback_query(F.data.startswith("movies:"))
async def callback_movies(callback: CallbackQuery):
    """Handle movies pagination"""
    page = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_movies(callback.message, page=page, edit=True, lang=user_lang)
    await callback.answer()


@router.callback_query(F.data.startswith("popular_movies:"))
async def callback_popular_movies(callback: CallbackQuery):
    """Handle popular movies pagination"""
    page = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_popular_movies(callback.message, page=page, edit=True, lang=user_lang)
    await callback.answer()


@router.callback_query(F.data.startswith("details_movie:"))
async def callback_movie_details(callback: CallbackQuery):
    """Handle movie details"""
    movie_id = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    await show_movie_details(callback.message, movie_id, edit=True, lang=user_lang)
    await callback.answer()


@router.callback_query(F.data.startswith("trailer_movie:"))
async def callback_movie_trailer(callback: CallbackQuery):
    """Handle movie trailer request"""
    movie_id = int(callback.data.split(":")[1])
    user_lang = get_user_language(callback.from_user.id)
    tmdb_lang = get_tmdb_language(user_lang)
    
    videos = await tmdb.get_movie_videos(movie_id, language=tmdb_lang)
    results = videos.get("results", [])
    
    # Find YouTube trailer
    trailer = None
    for video in results:
        if video.get("site") == "YouTube" and video.get("type") == "Trailer":
            trailer = video
            break
    
    # If no trailer in user language, try English
    if not trailer:
        videos = await tmdb.get_movie_videos(movie_id, language="en-US")
        results = videos.get("results", [])
        for video in results:
            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                trailer = video
                break
    
    if trailer:
        youtube_url = f"https://www.youtube.com/watch?v={trailer['key']}"
        await callback.answer(get_text(user_lang, "opening_trailer"), show_alert=False)
        await callback.message.answer(f"🎬 <b>Trailer</b>\n\n{youtube_url}", parse_mode="HTML")
    else:
        await callback.answer(get_text(user_lang, "no_trailer"), show_alert=True)


async def show_movies(message: Message, page: int = 1, edit: bool = False, lang: str = "en"):
    """Show latest movies (now playing)"""
    tmdb_lang = get_tmdb_language(lang)
    data = await tmdb.get_now_playing_movies(page=page, language=tmdb_lang)
    results = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 50)  # Cap at 50 pages
    
    if not results:
        text = get_text(lang, "no_movies")
        keyboard = get_back_keyboard(lang)
    else:
        movie = results[0]
        text = f"{get_text(lang, 'now_playing')}\n\n{tmdb.format_movie(movie, lang)}"
        keyboard = get_movies_keyboard(
            page=page,
            total_pages=total_pages,
            movie_id=movie.get("id"),
            has_trailer=True,
            lang=lang
        )
    
    if edit:
        # Try to edit with photo, fallback to text
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


async def show_popular_movies(message: Message, page: int = 1, edit: bool = False, lang: str = "en"):
    """Show popular movies"""
    tmdb_lang = get_tmdb_language(lang)
    data = await tmdb.get_popular_movies(page=page, language=tmdb_lang)
    results = data.get("results", [])
    total_pages = min(data.get("total_pages", 1), 50)
    
    if not results:
        text = get_text(lang, "no_movies")
        keyboard = get_back_keyboard(lang)
    else:
        movie = results[0]
        text = f"{get_text(lang, 'popular_movies_title')}\n\n{tmdb.format_movie(movie, lang)}"
        keyboard = get_popular_movies_keyboard(
            page=page,
            total_pages=total_pages,
            movie_id=movie.get("id"),
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


async def show_movie_details(message: Message, movie_id: int, edit: bool = False, lang: str = "en"):
    """Show detailed movie information"""
    tmdb_lang = get_tmdb_language(lang)
    movie = await tmdb.get_movie_details(movie_id, language=tmdb_lang)
    
    if "error" in movie or not movie.get("title"):
        text = get_text(lang, "no_movies")
        keyboard = get_back_keyboard(lang)
    else:
        title = movie.get("title", "Unknown")
        rating = movie.get("vote_average", 0)
        release_date = movie.get("release_date", "N/A")
        runtime = movie.get("runtime", 0)
        genres = ", ".join([g["name"] for g in movie.get("genres", [])[:3]])
        overview = movie.get("overview", "No description available.")
        
        text = (
            f"🎬 <b>{title}</b>\n\n"
            f"{get_text(lang, 'rating')}: {rating:.1f}/10\n"
            f"{get_text(lang, 'release')}: {release_date}\n"
            f"{get_text(lang, 'runtime')}: {runtime} min\n"
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
