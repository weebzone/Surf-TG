
import time
from aiohttp.web import Application
from cryptography.fernet import Fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from bot import LOGGER
from bot.config import Telegram
from bot.helper.utils import get_readable_time
from bot.helper.index import get_files
from bot.server.stream_routes import routes

secret_key = Fernet.generate_key()

async def web_server():
    web_app = Application(client_max_size=30000000)
    setup(web_app, EncryptedCookieStorage(Fernet(secret_key)))
    web_app.add_routes(routes)
    return web_app

async def indexing():
    for channel_id in Telegram.AUTH_CHANNEL:
        LOGGER.info(f'Start Indexing the Channel {channel_id}')
        start_time = time.time()
        await get_files(channel_id)
        end_time = time.time()
        elapsed_time = end_time - start_time
        LOGGER.info(f'Done Channel {channel_id}. Elapsed Time: {get_readable_time(elapsed_time)}')
