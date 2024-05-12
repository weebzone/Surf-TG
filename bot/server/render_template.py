from aiofiles import open as aiopen
from os import path as ospath

from bot import LOGGER
from bot.config import Telegram
from bot.helper.exceptions import InvalidHash
from bot.helper.utils import get_readable_file_size
from bot.server.file_properties import get_file_ids
from bot.telegram import StreamBot



admin_block = """
                    <style>
                        .admin-only {
                            display: none;
                        }
                    </style>"""


async def render_page(id, secure_hash, is_admin=False, html='', playlist='', database='', route='', redirect_url='', msg='', chat_id=''):
    tpath = ospath.join('bot', 'server', 'template')
    if route == 'login':
        async with aiopen(ospath.join(tpath, 'login.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Error -->", msg or '').replace("<!-- Theme -->", Telegram.THEME).replace("<!-- RedirectURL -->", redirect_url)
    elif route == 'home':
        async with aiopen(ospath.join(tpath, 'home.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Print -->", html).replace("<!-- Theme -->", Telegram.THEME).replace("<!-- Playlist -->", playlist)
            if not is_admin:
                html += admin_block
    elif route == 'playlist':
        async with aiopen(ospath.join(tpath, 'playlist.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Theme -->", Telegram.THEME).replace("<!-- Playlist -->", playlist).replace("<!-- Database -->", database).replace("<!-- Title -->", msg).replace("<!-- Parent_id -->", id)
            if not is_admin:
                html += admin_block
    elif route == 'index':
        async with aiopen(ospath.join(tpath, 'index.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Print -->", html).replace("<!-- Theme -->", Telegram.THEME).replace("<!-- Title -->", msg).replace("<!-- Chat_id -->", chat_id)
            if not is_admin:
                html += admin_block
    else:
        file_data = await get_file_ids(StreamBot, chat_id=int(chat_id), message_id=int(id))
        if file_data.unique_id[:6] != secure_hash:
            LOGGER.info('Link hash: %s - %s', secure_hash,
                        file_data.unique_id[:6])
            LOGGER.info('Invalid hash for message with - ID %s', id)
            raise InvalidHash
        filename, tag, size = file_data.file_name, file_data.mime_type.split(
            '/')[0].strip(), get_readable_file_size(file_data.file_size)
        if tag == 'video':
            async with aiopen(ospath.join(tpath, 'video.html')) as r:
                poster = f"/api/thumb/{chat_id}?id={id}"
                html = (await r.read()).replace('<!-- Filename -->', filename).replace("<!-- Theme -->", Telegram.THEME).replace('<!-- Poster -->', poster).replace('<!-- Size -->', size).replace('<!-- Username -->', StreamBot.me.username)
        else:
            async with aiopen(ospath.join(tpath, 'dl.html')) as r:
                html = (await r.read()).replace('<!-- Filename -->', filename).replace("<!-- Theme -->", Telegram.THEME).replace('<!-- Size -->', size)
    return html