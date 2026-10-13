from __future__ import annotations

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.constants import ERROR_TEXT
from src.logger import get_logger

logger = get_logger(__name__)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Unhandled exception", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                ERROR_TEXT, parse_mode=ParseMode.HTML
            )
        except Exception:  # pragma: no cover
            logger.warning("Failed to deliver error notice", exc_info=True)