from __future__ import annotations

from src.core import build_application
from src.logger import get_logger

logger = get_logger("premium-emoji-bot")


def main() -> None:
    application = build_application()
    logger.info("Starting polling loop")
    application.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()