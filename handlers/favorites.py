"""
Favorites Handler - Manage user's favorite movies and series
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from tmdb_client import tmdb
from translations import get_text, get_tmdb_language
from user_prefs import (
    get_user_language, get_favorites, add_favorite, remove_favorite, is_favorite
)

router = Router()


def get_favorites_menu(lang: str = "en") -> InlineKeyboardMarkup:
    """Favorites menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎬 " + get_text(lang, "fav_movies"), callback_data="fav_list:movies"),
            InlineKeyboardButton(text="📺 " + get_text(lang, "fav_series"), callback_data="fav_list:series")
        ],
        [InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")]
    ])


def get_favorites_list_keyboard(favorites: list, media_type: str, page: int, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard for favorites list with pagination"""
    buttons = []
    
    # Items per page
    per_page = 5
    start = page * per_page
    end = start + per_page
    page_items = favorites[start:end]
    total_pages = (len(favorites) + per_page - 1) // per_page
    
    # List items as buttons
    for item in page_items:
        emoji = "🎬" if media_type == "movies" else "📺"
        title = item.get("title", "Unknown")[:30]
        buttons.append([
            InlineKeyboardButton(
                text=f"{emoji} {title}",
                callback_data=f"fav_view:{media_type}:{item.get('id')}"
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=f"fav_remove:{media_type}:{item.get('id')}"
            )
        ])
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"fav_page:{media_type}:{page-1}"))
    if total_pages > 1:
        nav_row.append(InlineKeyboardButton(text=f"📄 {page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"fav_page:{media_type}:{page+1}"))
    if nav_row:
        buttons.append(nav_row)
    
    # Back button
    buttons.append([InlineKeyboardButton(text="⬅️ " + get_text(lang, "back"), callback_data="favorites")])
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("favorites"))
async def cmd_favorites(message: Message):
    """Handle /favorites command"""
    user_lang = get_user_language(message.from_user.id)
    
    text = f"⭐ <b>{get_text(user_lang, 'favorites')}</b>\n\n{get_text(user_lang, 'fav_description')}"
    
    await message.answer(
        text,
        reply_markup=get_favorites_menu(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "favorites")
async def callback_favorites(callback: CallbackQuery):
    """Handle favorites menu button"""
    user_lang = get_user_language(callback.from_user.id)
    
    text = f"⭐ <b>{get_text(user_lang, 'favorites')}</b>\n\n{get_text(user_lang, 'fav_description')}"
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_favorites_menu(user_lang),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=get_favorites_menu(user_lang),
            parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data.startswith("fav_list:"))
async def callback_favorites_list(callback: CallbackQuery):
    """Show favorites list"""
    media_type = callback.data.split(":")[1]
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    
    favorites = get_favorites(user_id, media_type)
    
    if not favorites:
        emoji = "🎬" if media_type == "movies" else "📺"
        text = f"{emoji} <b>{get_text(user_lang, 'fav_' + media_type)}</b>\n\n{get_text(user_lang, 'fav_empty')}"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ " + get_text(user_lang, "back"), callback_data="favorites")],
            [InlineKeyboardButton(text=get_text(user_lang, "main_menu"), callback_data="main_menu")]
        ])
    else:
        emoji = "🎬" if media_type == "movies" else "📺"
        text = f"{emoji} <b>{get_text(user_lang, 'fav_' + media_type)}</b>\n\n{get_text(user_lang, 'fav_count').format(count=len(favorites))}"
        keyboard = get_favorites_list_keyboard(favorites, media_type, 0, user_lang)
    
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("fav_page:"))
async def callback_favorites_page(callback: CallbackQuery):
    """Handle favorites pagination"""
    parts = callback.data.split(":")
    media_type = parts[1]
    page = int(parts[2])
    
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    favorites = get_favorites(user_id, media_type)
    
    emoji = "🎬" if media_type == "movies" else "📺"
    text = f"{emoji} <b>{get_text(user_lang, 'fav_' + media_type)}</b>\n\n{get_text(user_lang, 'fav_count').format(count=len(favorites))}"
    keyboard = get_favorites_list_keyboard(favorites, media_type, page, user_lang)
    
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception:
        pass
    await callback.answer()


@router.callback_query(F.data.startswith("fav_add:"))
async def callback_add_favorite(callback: CallbackQuery):
    """Add item to favorites"""
    parts = callback.data.split(":")
    media_type = parts[1]
    item_id = int(parts[2])
    
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    tmdb_lang = get_tmdb_language(user_lang)
    
    # Get item details
    if media_type == "movies":
        item = await tmdb.get_movie_details(item_id, language=tmdb_lang)
        title = item.get("title", "Unknown")
    else:
        item = await tmdb.get_series_details(item_id, language=tmdb_lang)
        title = item.get("name", "Unknown")
    
    poster_path = item.get("poster_path")
    
    if add_favorite(user_id, media_type, item_id, title, poster_path):
        await callback.answer(f"⭐ {get_text(user_lang, 'fav_added')}", show_alert=True)
    else:
        await callback.answer(f"ℹ️ {get_text(user_lang, 'fav_already')}", show_alert=True)


@router.callback_query(F.data.startswith("fav_remove:"))
async def callback_remove_favorite(callback: CallbackQuery):
    """Remove item from favorites"""
    parts = callback.data.split(":")
    media_type = parts[1]
    item_id = int(parts[2])
    
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    
    if remove_favorite(user_id, media_type, item_id):
        await callback.answer(f"🗑️ {get_text(user_lang, 'fav_removed')}", show_alert=True)
        
        # Refresh the list
        favorites = get_favorites(user_id, media_type)
        
        if not favorites:
            emoji = "🎬" if media_type == "movies" else "📺"
            text = f"{emoji} <b>{get_text(user_lang, 'fav_' + media_type)}</b>\n\n{get_text(user_lang, 'fav_empty')}"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ " + get_text(user_lang, "back"), callback_data="favorites")],
                [InlineKeyboardButton(text=get_text(user_lang, "main_menu"), callback_data="main_menu")]
            ])
        else:
            emoji = "🎬" if media_type == "movies" else "📺"
            text = f"{emoji} <b>{get_text(user_lang, 'fav_' + media_type)}</b>\n\n{get_text(user_lang, 'fav_count').format(count=len(favorites))}"
            keyboard = get_favorites_list_keyboard(favorites, media_type, 0, user_lang)
        
        try:
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        except Exception:
            pass
    else:
        await callback.answer("❌ Error", show_alert=True)


@router.callback_query(F.data.startswith("fav_view:"))
async def callback_view_favorite(callback: CallbackQuery):
    """View favorite item details"""
    parts = callback.data.split(":")
    media_type = parts[1]
    item_id = int(parts[2])
    
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    tmdb_lang = get_tmdb_language(user_lang)
    
    # Get item details
    if media_type == "movies":
        item = await tmdb.get_movie_details(item_id, language=tmdb_lang)
        title = item.get("title", "Unknown")
        rating = item.get("vote_average", 0)
        date = item.get("release_date", "N/A")
        runtime = item.get("runtime", 0)
        genres = ", ".join([g["name"] for g in item.get("genres", [])[:3]])
        overview = item.get("overview", "No description available.")
        
        text = (
            f"🎬 <b>{title}</b>\n\n"
            f"{get_text(user_lang, 'rating')}: {rating:.1f}/10\n"
            f"{get_text(user_lang, 'release')}: {date}\n"
            f"{get_text(user_lang, 'runtime')}: {runtime} min\n"
            f"{get_text(user_lang, 'genres')}: {genres}\n\n"
            f"{get_text(user_lang, 'overview')}\n{overview}"
        )
    else:
        item = await tmdb.get_series_details(item_id, language=tmdb_lang)
        title = item.get("name", "Unknown")
        rating = item.get("vote_average", 0)
        date = item.get("first_air_date", "N/A")
        seasons = item.get("number_of_seasons", 0)
        episodes = item.get("number_of_episodes", 0)
        genres = ", ".join([g["name"] for g in item.get("genres", [])[:3]])
        overview = item.get("overview", "No description available.")
        
        text = (
            f"📺 <b>{title}</b>\n\n"
            f"{get_text(user_lang, 'rating')}: {rating:.1f}/10\n"
            f"{get_text(user_lang, 'first_aired')}: {date}\n"
            f"{get_text(user_lang, 'seasons')}: {seasons} | {get_text(user_lang, 'episodes')}: {episodes}\n"
            f"{get_text(user_lang, 'genres')}: {genres}\n\n"
            f"{get_text(user_lang, 'overview')}\n{overview}"
        )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ " + get_text(user_lang, "fav_remove_btn"), callback_data=f"fav_remove:{media_type}:{item_id}")],
        [InlineKeyboardButton(text="⬅️ " + get_text(user_lang, "back"), callback_data=f"fav_list:{media_type}")],
        [InlineKeyboardButton(text=get_text(user_lang, "main_menu"), callback_data="main_menu")]
    ])
    
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception:
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
