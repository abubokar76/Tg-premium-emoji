from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

from src.constants import (
    ABOUT_TEXT,
    Callback,
    FEATURES_TEXT,
    HELP_TEXT,
    WELCOME_TEXT,
)
from src.keyboards import back_to_menu, main_menu


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None or query.data is None:
        return
    await query.answer()

    if query.data == Callback.MENU_HOME:
        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu(),
            disable_web_page_preview=True,
        )
    elif query.data == Callback.MENU_HELP:
        await query.edit_message_text(
            HELP_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_to_menu(),
            disable_web_page_preview=True,
        )
    elif query.data == Callback.MENU_FEATURES:
        await query.edit_message_text(
            FEATURES_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_to_menu(),
            disable_web_page_preview=True,
        )
    elif query.data == Callback.MENU_ABOUT:
        await query.edit_message_text(
            ABOUT_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=back_to_menu(),
            disable_web_page_preview=True,
        )


def register(application) -> None:
    application.add_handler(CallbackQueryHandler(on_callback))