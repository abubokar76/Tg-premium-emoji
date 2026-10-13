from __future__ import annotations

import logging
import sys

from src.config import config

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    logging.basicConfig(
        level=config.log_level,
        format=_FORMAT,
        datefmt=_DATEFMT,
        stream=sys.stdout,
        force=True,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram.ext.Application").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)