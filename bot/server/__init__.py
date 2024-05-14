from aiohttp.web import Application
from cryptography.fernet import Fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from bot.server.stream_routes import routes

secret_key = Fernet.generate_key()

async def web_server():
    web_app = Application(client_max_size=30000000)
    setup(web_app, EncryptedCookieStorage(Fernet(secret_key)))
    web_app.add_routes(routes)
    return web_app
