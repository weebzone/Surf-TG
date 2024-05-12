from asyncio import get_event_loop, sleep as asleep, gather, create_task
from traceback import format_exc

from aiohttp import web
from pyrogram import idle

from bot import __version__, LOGGER
from bot.config import Telegram
from bot.server import indexing, web_server
from bot.telegram import StreamBot
from bot.telegram.clients import initialize_clients

loop = get_event_loop()


async def start_services():
    LOGGER.info(f'Initializing Surf-TG v-{__version__}')
    await asleep(1.2)

    await gather(StreamBot.start())
    StreamBot.username = StreamBot.me.username
    LOGGER.info(f"Bot Client : {StreamBot.username}")

    await asleep(1.2)
    LOGGER.info("Initializing Multi Clients")
    await initialize_clients()

    await asleep(2)
    LOGGER.info('Initalizing Surf Web Server..')
    server = web.AppRunner(await web_server())
    LOGGER.info("Server CleanUp!")
    await server.cleanup()

    await asleep(2)
    LOGGER.info("Server Setup Started !")

    await server.setup()
    await web.TCPSite(server, '0.0.0.0', Telegram.PORT).start()
    await asleep(2)
    LOGGER.info("Start initial indexing. It will take time depending on the number of files in each channel.")

    tasks = [create_task(indexing(channel_id)) for channel_id in Telegram.AUTH_CHANNEL]
    await gather(*tasks)

    await asleep(2)
    LOGGER.info("Done You are ready to use the Surf-TG !")

    await idle()


async def stop_clients():
    await gather(StreamBot.stop())

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        LOGGER.info('Service Stopping...')
    except Exception as err:
        LOGGER.error(format_exc())
    finally:
        loop.run_until_complete(stop_clients())
        loop.stop()
