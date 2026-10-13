# Premium Emoji Bot

Production-grade Telegram bot that extracts custom emoji metadata from forwarded messages.

## Features

- Fully async handlers (python-telegram-bot v21)
- Structured logging with configurable level
- Per-user rate limiting (TTL cache)
- AIO rate limiter for outgoing traffic
- Inline menu with callbacks
- Global error handler
- Docker-ready

## Setup

```bash
git clone <repo>
cd premium-emoji-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add BOT_TOKEN
python main.py
```

## Docker

```bash
docker build -t premium-emoji-bot .
docker run --env-file .env premium-emoji-bot
```

## Notes

Telegram does not expose custom emoji as downloadable media through the Bot API.
This bot therefore returns the canonical `custom_emoji_id` for every detected
emoji, which is the only reliable identifier available to bots.