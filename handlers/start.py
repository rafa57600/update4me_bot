"""
Start Handler - Welcome message and main menu - Localized
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from keyboards.inline import get_main_menu_localized
from translations import get_text
from user_prefs import get_user_language

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    user_lang = get_user_language(message.from_user.id)
    welcome = get_text(user_lang, "welcome")
    
    await message.answer(
        welcome,
        reply_markup=get_main_menu_localized(user_lang),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    user_lang = get_user_language(message.from_user.id)
    welcome = get_text(user_lang, "welcome")
    
    await message.answer(
        welcome,
        reply_markup=get_main_menu_localized(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery):
    """Handle main menu button"""
    user_lang = get_user_language(callback.from_user.id)
    welcome = get_text(user_lang, "welcome")
    
    try:
        # Try to edit text (works for text messages)
        await callback.message.edit_text(
            welcome,
            reply_markup=get_main_menu_localized(user_lang),
            parse_mode="HTML"
        )
    except Exception:
        # If it's a photo message, delete and send new message
        await callback.message.delete()
        await callback.message.answer(
            welcome,
            reply_markup=get_main_menu_localized(user_lang),
            parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def callback_noop(callback: CallbackQuery):
    """Handle no-operation callbacks (like page indicator)"""
    await callback.answer()
