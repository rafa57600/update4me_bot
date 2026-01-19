"""
Subscriptions Handler - Manage user subscription topics
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from translations import get_text
from user_prefs import (
    get_user_language, get_subscriptions, add_subscription, 
    remove_subscription, is_subscribed, SUBSCRIPTION_TOPICS
)

router = Router()


def get_subscriptions_keyboard(user_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    """Subscriptions menu keyboard showing all topics with toggle"""
    buttons = []
    user_subs = get_subscriptions(user_id)
    
    # Group topics in rows of 2
    topics = list(SUBSCRIPTION_TOPICS.items())
    for i in range(0, len(topics), 2):
        row = []
        for topic_key, topic_info in topics[i:i+2]:
            is_sub = topic_key in user_subs
            emoji = topic_info["emoji"]
            check = "✅" if is_sub else "⬜"
            name = get_text(lang, topic_info["name_key"])
            
            row.append(InlineKeyboardButton(
                text=f"{check} {emoji} {name}",
                callback_data=f"sub_toggle:{topic_key}"
            ))
        buttons.append(row)
    
    # My subscriptions button
    buttons.append([InlineKeyboardButton(
        text="📋 " + get_text(lang, "my_subscriptions"),
        callback_data="sub_my"
    )])
    
    # Back to menu
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_my_subscriptions_keyboard(user_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard showing user's active subscriptions"""
    buttons = []
    user_subs = get_subscriptions(user_id)
    
    if user_subs:
        for topic_key in user_subs:
            if topic_key in SUBSCRIPTION_TOPICS:
                topic_info = SUBSCRIPTION_TOPICS[topic_key]
                emoji = topic_info["emoji"]
                name = get_text(lang, topic_info["name_key"])
                
                buttons.append([
                    InlineKeyboardButton(
                        text=f"{emoji} {name}",
                        callback_data="noop"
                    ),
                    InlineKeyboardButton(
                        text="🔕 " + get_text(lang, "unsubscribe"),
                        callback_data=f"sub_off:{topic_key}"
                    )
                ])
    
    # Back button
    buttons.append([InlineKeyboardButton(text="⬅️ " + get_text(lang, "back"), callback_data="subscriptions")])
    buttons.append([InlineKeyboardButton(text=get_text(lang, "main_menu"), callback_data="main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("subscriptions"))
async def cmd_subscriptions(message: Message):
    """Handle /subscriptions command"""
    user_lang = get_user_language(message.from_user.id)
    user_subs = get_subscriptions(message.from_user.id)
    
    text = (
        f"🔔 <b>{get_text(user_lang, 'subscriptions')}</b>\n\n"
        f"{get_text(user_lang, 'sub_description')}\n\n"
        f"📊 {get_text(user_lang, 'sub_active')}: {len(user_subs)}"
    )
    
    await message.answer(
        text,
        reply_markup=get_subscriptions_keyboard(message.from_user.id, user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "subscriptions")
async def callback_subscriptions(callback: CallbackQuery):
    """Handle subscriptions menu button"""
    user_lang = get_user_language(callback.from_user.id)
    user_subs = get_subscriptions(callback.from_user.id)
    
    text = (
        f"🔔 <b>{get_text(user_lang, 'subscriptions')}</b>\n\n"
        f"{get_text(user_lang, 'sub_description')}\n\n"
        f"📊 {get_text(user_lang, 'sub_active')}: {len(user_subs)}"
    )
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_subscriptions_keyboard(callback.from_user.id, user_lang),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=get_subscriptions_keyboard(callback.from_user.id, user_lang),
            parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data.startswith("sub_toggle:"))
async def callback_toggle_subscription(callback: CallbackQuery):
    """Toggle subscription on/off"""
    topic = callback.data.split(":")[1]
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    
    if is_subscribed(user_id, topic):
        remove_subscription(user_id, topic)
        await callback.answer(f"🔕 {get_text(user_lang, 'unsubscribed')}", show_alert=False)
    else:
        add_subscription(user_id, topic)
        await callback.answer(f"🔔 {get_text(user_lang, 'subscribed')}", show_alert=False)
    
    # Refresh the menu
    user_subs = get_subscriptions(user_id)
    text = (
        f"🔔 <b>{get_text(user_lang, 'subscriptions')}</b>\n\n"
        f"{get_text(user_lang, 'sub_description')}\n\n"
        f"📊 {get_text(user_lang, 'sub_active')}: {len(user_subs)}"
    )
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_subscriptions_keyboard(user_id, user_lang),
            parse_mode="HTML"
        )
    except Exception:
        pass


@router.callback_query(F.data == "sub_my")
async def callback_my_subscriptions(callback: CallbackQuery):
    """Show user's active subscriptions"""
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    user_subs = get_subscriptions(user_id)
    
    if user_subs:
        text = (
            f"📋 <b>{get_text(user_lang, 'my_subscriptions')}</b>\n\n"
            f"{get_text(user_lang, 'sub_manage')}"
        )
    else:
        text = (
            f"📋 <b>{get_text(user_lang, 'my_subscriptions')}</b>\n\n"
            f"{get_text(user_lang, 'sub_empty')}"
        )
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_my_subscriptions_keyboard(user_id, user_lang),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=get_my_subscriptions_keyboard(user_id, user_lang),
            parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data.startswith("sub_off:"))
async def callback_unsubscribe(callback: CallbackQuery):
    """Unsubscribe from a topic"""
    topic = callback.data.split(":")[1]
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id)
    
    remove_subscription(user_id, topic)
    await callback.answer(f"🔕 {get_text(user_lang, 'unsubscribed')}", show_alert=False)
    
    # Refresh the list
    user_subs = get_subscriptions(user_id)
    
    if user_subs:
        text = (
            f"📋 <b>{get_text(user_lang, 'my_subscriptions')}</b>\n\n"
            f"{get_text(user_lang, 'sub_manage')}"
        )
    else:
        text = (
            f"📋 <b>{get_text(user_lang, 'my_subscriptions')}</b>\n\n"
            f"{get_text(user_lang, 'sub_empty')}"
        )
    
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_my_subscriptions_keyboard(user_id, user_lang),
            parse_mode="HTML"
        )
    except Exception:
        pass
