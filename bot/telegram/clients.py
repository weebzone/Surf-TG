from asyncio import sleep as asleep, gather
from pyrogram import Client

from bot import LOGGER
from bot.config import Telegram
from bot.helper.parser import TokenParser
from bot.telegram import multi_clients, work_loads, StreamBot


async def initialize_clients():
    multi_clients[0], work_loads[0] = StreamBot, 0
    all_tokens = TokenParser().parse_from_env()
    if not all_tokens:
        LOGGER.info("No additional Bot Clients found, Using default client")
        return

    async def start_client(client_id, token):
        try:
            LOGGER.info(f"Starting - Bot Client {client_id}")
            if client_id == len(all_tokens):
                await asleep(2)
            client = await Client(
                name=str(client_id),
                api_id=Telegram.API_ID,
                api_hash=Telegram.API_HASH,
                bot_token=token,
                sleep_threshold=Telegram.SLEEP_THRESHOLD,
                no_updates=True,
                in_memory=True
            ).start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            LOGGER.error(
                f"Failed starting Client - {client_id} Error:", exc_info=True)

    clients = await gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        Telegram.MULTI_CLIENT = True
        LOGGER.info("Multi-Client Mode Enabled")
    else:
        LOGGER.info(
            "No additional clients were initialized, using default client")
