from pyrogram import Client
from bot.config import Telegram


plugins = {"root": "bot/telegram/plugins"}

StreamBot = Client(
    name='bot',
    api_id=Telegram.API_ID,
    api_hash=Telegram.API_HASH,
    bot_token=Telegram.BOT_TOKEN,
    workdir="bot",
    plugins=plugins,
    sleep_threshold=Telegram.SLEEP_THRESHOLD,
    workers=Telegram.WORKERS,
    max_concurrent_transmissions=1000
)
UserBot = Client(
    name='user',
    api_id=Telegram.API_ID,
    api_hash=Telegram.API_HASH,
    session_string=Telegram.SESSION_STRING,
    sleep_threshold=Telegram.SLEEP_THRESHOLD,
    no_updates=True,
    in_memory=True,
)

multi_clients = {}
work_loads = {}
