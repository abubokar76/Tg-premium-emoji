from __future__ import annotations

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from src.constants import Callback


# ─────────────────────────────────────────────────────────────
#  Inline Keyboards (message er niche)
# ─────────────────────────────────────────────────────────────

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📖 Help", callback_data=Callback.MENU_HELP),
                InlineKeyboardButton("💎 Features", callback_data=Callback.MENU_FEATURES),
            ],
            [
                InlineKeyboardButton("ℹ️ About", callback_data=Callback.MENU_ABOUT),
            ],
        ]
    )


def back_to_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅️ Back to Menu", callback_data=Callback.MENU_HOME),
            ]
        ]
    )


# ─────────────────────────────────────────────────────────────
#  Reply Keyboard (chat er niche sob command button)
# ─────────────────────────────────────────────────────────────

def reply_keyboard() -> ReplyKeyboardMarkup:
    """Colorful persistent keyboard with all commands as buttons."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("🏠 Start"),
                KeyboardButton("📖 Help"),
            ],
            [
                KeyboardButton("💎 Features"),
                KeyboardButton("ℹ️ About"),
            ],
            [
                KeyboardButton("📊 Stats"),
                KeyboardButton("⚡ Ping"),
            ],
            [
                KeyboardButton("🆔 My ID"),
                KeyboardButton("❌ Close Keyboard"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="✨ Choose an option...",
        is_persistent=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()