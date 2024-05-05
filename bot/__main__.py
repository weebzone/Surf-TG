import asyncio
import logging
import traceback
from aiohttp import web
from bot.config import Telegram
from bot.server import web_server
from bot.telegram import StreamBot, UserBot
from bot.telegram.clients import initialize_clients
from pyrogram import idle
from bot import __version__

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)


StreamBot.start()
UserBot.start()
loop = asyncio.get_event_loop()


async def start_services():
    print(f'------------------- Surf-TG v-{__version__} -------------------')
    print('\n')
    print('------------------- Initalizing Telegram Bot and User Bot -------------------')
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    await asyncio.sleep(2)
    print(f"Start Main Bot Client {StreamBot.username}")
    user_info = await UserBot.get_me()
    UserBot.username = user_info.username or user_info.first_name or user_info.id
    await asyncio.sleep(2)
    print(f"Start Main User Client {UserBot.username}")
    print("------------------------------ DONE ------------------------------")
    print()
    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    print('')
    print('-------------------- Initalizing Web Server -------------------------')
    await asyncio.sleep(2)
    server = web.AppRunner(await web_server())
    print("Server CleanUp")
    await server.cleanup()
    await asyncio.sleep(2)
    print("Server Setup")
    await server.setup()
    await web.TCPSite(server, '0.0.0.0', Telegram.PORT).start()
    print("------------------------------ DONE ------------------------------")
    await idle()


async def cleanup():
    await StreamBot.stop()
    await asyncio.sleep(2)
    await UserBot.stop()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        logging.info('----------------------- Service Stopping -----------------------')
    except Exception as err:
        logging.error(traceback.format_exc())
    finally:
        loop.run_until_complete(cleanup())
        loop.stop()
        print("------------------------ Done ------------------------")
