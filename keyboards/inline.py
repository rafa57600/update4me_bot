"""
Inline Keyboard Builders for Telegram Bot
Beautiful UI components with navigation - Localized version
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional

from translations import get_text


def get_main_menu_localized(lang: str = "en") -> InlineKeyboardMarkup:
    """Main menu keyboard - localized"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text(lang, "latest_movies"), callback_data="movies:1"),
            InlineKeyboardButton(text=get_text(lang, "latest_series"), callback_data="series:1")
        ],
        [
            InlineKeyboardButton(text=get_text(lang, "trending"), callback_data="trending:1"),
            InlineKeyboardButton(text=get_text(lang, "search"), switch_inline_query_current_chat="")
        ],
        [
            InlineKeyboardButton(text=get_text(lang, "popular_movies"), callback_data="popular_movies:1"),
            InlineKeyboardButton(text=get_text(lang, "popular_series"), callback_data="popular_series:1")
        ],
        [
            InlineKeyboardButton(text="⭐ " + get_text(lang, "favorites"), callback_data="favorites"),
            InlineKeyboardButton(text="🔔 " + get_text(lang, "subscriptions"), callback_data="subscriptions")
        ],
        [
            InlineKeyboardButton(text=get_text(lang, "language"), callback_data="language")
        ]
    ])


def get_main_menu() -> InlineKeyboardMarkup:
    """Main menu keyboard - default English"""
    return get_main_menu_localized("en")


def get_movies_keyboard(
    page: int,
    total_pages: int,
    movie_id: Optional[int] = None,
    has_trailer: bool = False,
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Keyboard for movie display with navigation"""
    buttons = []
    
    # Action buttons row
    action_row = []
    if has_trailer and movie_id:
        action_row.append(InlineKeyboardButton(text=get_text(lang, "trailer"), callback_data=f"trailer_movie:{movie_id}"))
    if movie_id:
        action_row.append(InlineKeyboardButton(text=get_text(lang, "details"), callback_data=f"details_movie:{movie_id}"))
    if action_row:
        buttons.append(action_row)
    
    # Navigation row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "previous"), callback_data=f"movies:{page-1}"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "next"), callback_data=f"movies:{page+1}"))
    buttons.append(nav_row)
    
    # Back to menu
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_series_keyboard(
    page: int,
    total_pages: int,
    series_id: Optional[int] = None,
    has_trailer: bool = False,
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Keyboard for series display with navigation"""
    buttons = []
    
    # Action buttons row
    action_row = []
    if has_trailer and series_id:
        action_row.append(InlineKeyboardButton(text=get_text(lang, "trailer"), callback_data=f"trailer_series:{series_id}"))
    if series_id:
        action_row.append(InlineKeyboardButton(text=get_text(lang, "details"), callback_data=f"details_series:{series_id}"))
    if action_row:
        buttons.append(action_row)
    
    # Navigation row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "previous"), callback_data=f"series:{page-1}"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "next"), callback_data=f"series:{page+1}"))
    buttons.append(nav_row)
    
    # Back to menu
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_trending_keyboard(
    page: int,
    total_pages: int,
    item_id: Optional[int] = None,
    media_type: str = "movie",
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Keyboard for trending display with navigation"""
    buttons = []
    
    # Action buttons row
    action_row = []
    if item_id:
        action_row.append(InlineKeyboardButton(text=get_text(lang, "details"), callback_data=f"details_{media_type}:{item_id}"))
    if action_row:
        buttons.append(action_row)
    
    # Navigation row
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "previous"), callback_data=f"trending:{page-1}"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "next"), callback_data=f"trending:{page+1}"))
    buttons.append(nav_row)
    
    # Back to menu
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_popular_movies_keyboard(page: int, total_pages: int, movie_id: Optional[int] = None, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard for popular movies with navigation"""
    buttons = []
    
    if movie_id:
        buttons.append([InlineKeyboardButton(text=get_text(lang, "details"), callback_data=f"details_movie:{movie_id}")])
    
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "previous"), callback_data=f"popular_movies:{page-1}"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "next"), callback_data=f"popular_movies:{page+1}"))
    buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_popular_series_keyboard(page: int, total_pages: int, series_id: Optional[int] = None, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard for popular series with navigation"""
    buttons = []
    
    if series_id:
        buttons.append([InlineKeyboardButton(text=get_text(lang, "details"), callback_data=f"details_series:{series_id}")])
    
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "previous"), callback_data=f"popular_series:{page-1}"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "next"), callback_data=f"popular_series:{page+1}"))
    buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_search_results_keyboard(
    page: int, 
    total_pages: int, 
    query: str,
    item_id: Optional[int] = None,
    media_type: str = "movie",
    lang: str = "en"
) -> InlineKeyboardMarkup:
    """Keyboard for search results with navigation"""
    buttons = []
    
    if item_id:
        buttons.append([InlineKeyboardButton(text=get_text(lang, "details"), callback_data=f"details_{media_type}:{item_id}")])
    
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "previous"), callback_data=f"search:{query}:{page-1}"))
    nav_row.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text=get_text(lang, "next"), callback_data=f"search:{query}:{page+1}"))
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Simple back to menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")]
    ])
