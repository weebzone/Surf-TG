from asyncio import get_event_loop, sleep as asleep, gather
from traceback import format_exc

from aiohttp import web
from pyrogram import idle

from bot import __version__, LOGGER
from bot.config import Telegram
from bot.server import web_server
from bot.telegram import StreamBot, UserBot
from bot.telegram.clients import initialize_clients

loop = get_event_loop()

async def start_services():
    print(f'Initializing Surf-TG v-{__version__}')
    await asleep(1.2)
    
    await gather(StreamBot.start(), UserBot.start())
    StreamBot.username = StreamBot.me.username
    print(f"Bot Client : {StreamBot.username}")
    UserBot.username = UserBot.me.username or UserBot.me.first_name or UserBot.me.id
    print(f"User Client : {UserBot.username}")
    
    await asleep(1.2)
    print("Initializing Multi Clients")
    await initialize_clients()
    print("DONE")
    
    await asleep(2)
    print('Initalizing Surf Web Server')
    server = web.AppRunner(await web_server())
    print("Server CleanUp")
    await server.cleanup()
    
    await asyncio.sleep(2)
    print("Server Setup")
    
    await server.setup()
    await web.TCPSite(server, '0.0.0.0', Telegram.PORT).start()
    print("------------------------------ DONE ------------------------------")
    
    await idle()

async def stop_clients():
    await gather(StreamBot.stop(), UserBot.stop())

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        LOGGER.info('----------------------- Service Stopping -----------------------')
    except Exception as err:
        LOGGER.error(format_exc())
    finally:
        loop.run_until_complete(stop_clients())
        loop.stop()
        print("------------------------ Done ------------------------")
