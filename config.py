from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    log_level: str
    rate_limit_per_minute: int

    @classmethod
    def load(cls) -> "Config":
        token = os.getenv("BOT_TOKEN", "").strip()
        if not token:
            raise RuntimeError("BOT_TOKEN is missing in environment")

        return cls(
            bot_token=token,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "20")),
        )


config = Config.load()