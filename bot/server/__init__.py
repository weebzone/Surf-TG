from aiohttp import web

from bot.server.stream_routes import routes
from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

secret_key = fernet.Fernet.generate_key()
fernet_instance = fernet.Fernet(secret_key)

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    setup(web_app, EncryptedCookieStorage(fernet_instance))
    web_app.add_routes(routes)
    return web_app