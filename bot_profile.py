from __future__ import annotations

from telegram import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeDefault,
)
from telegram.ext import ContextTypes

from src.logger import get_logger

logger = get_logger(__name__)

BOT_NAME = "✨ AGS Premium Emoji"

BOT_ABOUT = (
    "🎨 Convert Telegram Premium custom emoji into reusable assets. "
    "Forward any premium emoji message and get instant metadata. ⚡"
)

BOT_DESCRIPTION = (
    "╔══════════════════════════╗\n"
    "║   ✨ PREMIUM EMOJI BOT ✨   ║\n"
    "╚══════════════════════════╝\n\n"
    "🎨 Convert Telegram Premium custom emoji\n"
    "into reusable assets — instantly.\n\n"
    "💎 FEATURES\n"
    " ├ 🆔 Unique emoji identifiers\n"
    " ├ 🖼 Reconstructed message preview\n"
    " ├ 🎞 Video sticker re-emission\n"
    " └ ⚡ Blazing-fast response\n\n"
    "🚀 HOW TO USE\n"
    " 1. 📋 Copy a message with premium emoji\n"
    " 2. 📤 Forward it to this bot\n"
    " 3. 🎁 Receive metadata instantly\n\n"
    "👇 Press START to begin"
)

# ─────────────────────────────────────────────────────────────
#  Colorful Bot Commands (Menu button e dekhabe)
# ─────────────────────────────────────────────────────────────

BOT_COMMANDS = [
    BotCommand("start",    "🏠 Open Main Menu"),
    BotCommand("help",     "📖 Help Center"),
    BotCommand("about",    "ℹ️ About This Bot"),
    BotCommand("features", "💎 Premium Features"),
    BotCommand("stats",    "📊 Bot Statistics"),
    BotCommand("ping",     "⚡ Speed Test"),
    BotCommand("id",       "🆔 Get Your User ID"),
]


async def setup_bot_profile(application) -> None:
    """Runs once on startup — sets name, about, description, commands."""
    bot = application.bot

    try:
        await bot.set_my_name(name=BOT_NAME)
        logger.info("Bot name updated")
    except Exception as exc:
        logger.warning("Could not set bot name: %s", exc)

    try:
        await bot.set_my_short_description(
            short_description="Convert Premium emoji into reusable assets ⚡"
        )
        logger.info("Bot short description updated")
    except Exception as exc:
        logger.warning("Could not set short description: %s", exc)

    try:
        await bot.set_my_description(description=BOT_DESCRIPTION)
        logger.info("Bot description updated")
    except Exception as exc:
        logger.warning("Could not set description: %s", exc)

    # ── Colorful commands menu (blue Menu button) ──
    for scope_name, scope in (
        ("default", BotCommandScopeDefault()),
        ("private", BotCommandScopeAllPrivateChats()),
        ("groups", BotCommandScopeAllGroupChats()),
    ):
        try:
            await bot.set_my_commands(commands=BOT_COMMANDS, scope=scope)
            logger.info("Commands registered for scope: %s", scope_name)
        except Exception as exc:
            logger.warning("Could not set commands for %s: %s", scope_name, exc)