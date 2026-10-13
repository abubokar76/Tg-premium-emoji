from __future__ import annotations

import time

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes

from src.constants import ABOUT_TEXT, FEATURES_TEXT, HELP_TEXT, WELCOME_TEXT
from src.keyboards import back_to_menu, main_menu, reply_keyboard, remove_keyboard

_START_TIME = time.time()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(
        WELCOME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_keyboard(),
        disable_web_page_preview=True,
    )
    await message.reply_text(
        "⌨️ <b>Quick actions:</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(
        HELP_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=back_to_menu(),
        disable_web_page_preview=True,
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(
        ABOUT_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=back_to_menu(),
        disable_web_page_preview=True,
    )


async def features(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(
        FEATURES_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=back_to_menu(),
        disable_web_page_preview=True,
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return

    uptime = int(time.time() - _START_TIME)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)

    text = (
        "╔══════════════════════════╗\n"
        "║      📊 <b>BOT STATS</b> 📊      ║\n"
        "╚══════════════════════════╝\n"
        "\n"
        "⚙️ <b>System Status</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  🟢 <b>Status:</b>      <code>Online</code>\n"
        f"  ⏱ <b>Uptime:</b>      <code>{hours}h {minutes}m {seconds}s</code>\n"
        f"  🐍 <b>Python:</b>      <code>3.13</code>\n"
        f"  📡 <b>Library:</b>     <code>PTB v21</code>\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💎 <i>All systems operational.</i>"
    )
    await message.reply_text(text, parse_mode=ParseMode.HTML)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return

    start = time.perf_counter()
    sent = await message.reply_text("🏓 <b>Pinging…</b>", parse_mode=ParseMode.HTML)
    elapsed = (time.perf_counter() - start) * 1000

    if elapsed < 200:
        grade = "🟢 Excellent"
    elif elapsed < 500:
        grade = "🟡 Good"
    else:
        grade = "🔴 Slow"

    await sent.edit_text(
        "╔══════════════════════════╗\n"
        "║       ⚡ <b>PONG!</b> ⚡       ║\n"
        "╚══════════════════════════╝\n"
        "\n"
        f"🚀 <b>Latency:</b> <code>{elapsed:.2f} ms</code>\n"
        f"📶 <b>Grade:</b> {grade}\n"
        "\n"
        "<i>Fast, isn't it?</i>",
        parse_mode=ParseMode.HTML,
    )


async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    if message is None or user is None:
        return

    chat = update.effective_chat
    chat_id = chat.id if chat else "N/A"

    text = (
        "╔══════════════════════════╗\n"
        "║      🆔 <b>YOUR IDENTITY</b>      ║\n"
        "╚══════════════════════════╝\n"
        "\n"
        f"👤 <b>Name:</b>  {user.full_name}\n"
        f"🆔 <b>User ID:</b>  <code>{user.id}</code>\n"
        f"💬 <b>Chat ID:</b>  <code>{chat_id}</code>\n"
    )
    if user.username:
        text += f"🔗 <b>Username:</b>  @{user.username}\n"

    text += (
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 <i>Tap the ID to copy it.</i>"
    )
    await message.reply_text(text, parse_mode=ParseMode.HTML)


async def close_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(
        "❌ <b>Keyboard hidden.</b>\n\n<i>Send /start to bring it back.</i>",
        parse_mode=ParseMode.HTML,
        reply_markup=remove_keyboard(),
    )


def register(application) -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("features", features))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("id", user_id))