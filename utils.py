from __future__ import annotations

import html
from dataclasses import dataclass
from typing import Iterable, Sequence

from telegram import MessageEntity

from src.config import config


def escape(value: str) -> str:
    return html.escape(value, quote=False)


def truncate(value: str, limit: int = 64) -> str:
    return value if len(value) <= limit else f"{value[: limit - 1]}…"


@dataclass(slots=True, frozen=True)
class PremiumEmoji:
    index: int
    emoji_id: str
    offset: int
    length: int
    source: str

    @classmethod
    def extract(
        cls, text: str, entities: Sequence[MessageEntity]
    ) -> list["PremiumEmoji"]:
        custom = [e for e in entities if e.type == MessageEntity.CUSTOM_EMOJI]
        custom.sort(key=lambda e: e.offset)

        results: list[PremiumEmoji] = []
        for idx, entity in enumerate(custom, start=1):
            results.append(
                cls(
                    index=idx,
                    emoji_id=entity.custom_emoji_id or "",
                    offset=entity.offset,
                    length=entity.length,
                    source=text[entity.offset : entity.offset + entity.length],
                )
            )
        return results


def render_premium_report(
    text: str,
    emojis: Iterable[PremiumEmoji],
    user_mention: str,
) -> str:
    emojis = list(emojis)
    highlighted = text
    for emoji in reversed(emojis):
        placeholder = f"⟦{emoji.index}⟧"
        highlighted = (
            highlighted[: emoji.offset]
            + placeholder
            + highlighted[emoji.offset + emoji.length :]
        )

    lines: list[str] = [
        "╔══════════════════════════╗",
        "║  ✅ <b>PREMIUM EMOJI FOUND</b>  ║",
        "╚══════════════════════════╝",
        "",
        f"👤 <b>Requested by:</b> {user_mention}",
        f"🔢 <b>Total detected:</b> <b>{len(emojis)}</b>",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "📝 <b>Reconstructed Text</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"<code>{escape(truncate(highlighted, 300))}</code>",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "🆔 <b>Emoji Identifiers</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]

    for emoji in emojis:
        lines.append(
            f"  <b>{emoji.index}.</b> 💎 <code>{escape(emoji.emoji_id)}</code>"
        )

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "💡 <i>Custom emoji cannot be rendered as",
            "standard Unicode — use these IDs with any",
            "API that supports Telegram custom emoji.</i>",
        ]
    )
    return "\n".join(lines)


def user_label(message) -> str:
    user = message.from_user
    if user is None:
        return "Anonymous"
    name = html.escape(user.full_name or user.first_name or "User")
    if user.username:
        return f'<a href="https://t.me/{user.username}">{name}</a>'
    return f'<a href="tg://user?id={user.id}">{name}</a>'


RATE_LIMIT = config.rate_limit_per_minute