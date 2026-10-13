from __future__ import annotations

from cachetools import TTLCache
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, MessageHandler, filters

from src.config import config
from src.constants import (
    NO_PREMIUM_TEXT,
    RATE_LIMIT_TEXT,
    STATIC_STICKER_TEXT,
    STICKER_SAVED_TEXT,
    UNSUPPORTED_TEXT,
)
from src.logger import get_logger
from src.utils import PremiumEmoji, render_premium_report, user_label

logger = get_logger(__name__)

_rate_cache: TTLCache[int, int] = TTLCache(maxsize=10_000, ttl=60)

# Map keyboard button text → command name
_KEYBOARD_BUTTONS = {
    "🏠 start": "start",
    "📖 help": "help",
    "💎 features": "features",
    "ℹ️ about": "about",
    "📊 stats": "stats",
    "⚡ ping": "ping",
    "🆔 my id": "id",
    "❌ close keyboard": "close_keyboard",
}


def _is_rate_limited(user_id: int) -> bool:
    count = _rate_cache.get(user_id, 0)
    if count >= config.rate_limit_per_minute:
        return True
    _rate_cache[user_id] = count + 1
    return False


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None or not message.text:
        return

    # ── Check if it's a keyboard button ──
    key = message.text.strip().lower()
    if key in _KEYBOARD_BUTTONS:
        from src.handlers import commands as cmd_module

        target = _KEYBOARD_BUTTONS[key]
        handler = getattr(cmd_module, target, None)
        if handler:
            await handler(update, context)
            return

    if _is_rate_limited(user.id):
        await message.reply_text(RATE_LIMIT_TEXT, parse_mode=ParseMode.HTML)
        return

    emojis = PremiumEmoji.extract(message.text, message.entities or [])
    if not emojis:
        await message.reply_text(NO_PREMIUM_TEXT, parse_mode=ParseMode.HTML)
        return

    logger.info("user=%s premium_emojis=%d", user.id, len(emojis))

    report = render_premium_report(
        text=message.text,
        emojis=emojis,
        user_mention=user_label(message),
    )
    await message.reply_text(
        report,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def on_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None or message.sticker is None:
        return

    sticker = message.sticker
    if sticker.is_video:
        await message.reply_sticker(sticker.file_id)
        await message.reply_text(
            STICKER_SAVED_TEXT,
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_text(
            STATIC_STICKER_TEXT,
            parse_mode=ParseMode.HTML,
        )


async def on_unsupported(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(UNSUPPORTED_TEXT, parse_mode=ParseMode.HTML)


def register(application) -> None:
    application.add_handler(
        MessageHandler(filters.Sticker.ALL & ~filters.COMMAND, on_sticker)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_text)
    )
    application.add_handler(
        MessageHandler(
            (filters.PHOTO | filters.VIDEO | filters.Document.ALL)
            & ~filters.COMMAND,
            on_unsupported,
        )
    )