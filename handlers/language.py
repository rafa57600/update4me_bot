"""
Language Handler - Language selection and settings
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from translations import SUPPORTED_LANGUAGES, get_text
from user_prefs import get_user_language, set_user_language
from keyboards.inline import get_main_menu_localized

router = Router()


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Create language selection keyboard"""
    buttons = []
    row = []
    
    for code, info in SUPPORTED_LANGUAGES.items():
        row.append(InlineKeyboardButton(
            text=info["name"],
            callback_data=f"set_lang:{code}"
        ))
        if len(row) == 2:  # 2 buttons per row
            buttons.append(row)
            row = []
    
    if row:  # Add remaining buttons
        buttons.append(row)
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("language"))
async def cmd_language(message: Message):
    """Handle /language command"""
    user_lang = get_user_language(message.from_user.id)
    text = get_text(user_lang, "select_language")
    
    await message.answer(
        text,
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "language")
async def callback_language(callback: CallbackQuery):
    """Handle language button from menu"""
    user_lang = get_user_language(callback.from_user.id)
    text = get_text(user_lang, "select_language")
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data.startswith("set_lang:"))
async def callback_set_language(callback: CallbackQuery):
    """Handle language selection"""
    lang_code = callback.data.split(":")[1]
    user_id = callback.from_user.id
    
    # Save preference
    set_user_language(user_id, lang_code)
    
    # Get confirmation message in new language
    lang_name = SUPPORTED_LANGUAGES[lang_code]["name"]
    
    # Show confirmation and return to main menu
    await callback.answer(f"✅ {lang_name}", show_alert=True)
    
    # Show main menu in new language
    welcome = get_text(lang_code, "welcome")
    
    try:
        await callback.message.edit_text(
            welcome,
            reply_markup=get_main_menu_localized(lang_code),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            welcome,
            reply_markup=get_main_menu_localized(lang_code),
            parse_mode="HTML"
        )
