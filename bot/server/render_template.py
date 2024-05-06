from aiofiles import open as aiopen
from os import path as ospath

from bot import LOGGER
from bot.config import Telegram
from bot.helper.exceptions import InvalidHash
from bot.helper.file_size import get_readable_file_size
from bot.server.file_properties import get_file_ids
from bot.telegram import StreamBot


async def render_page(message_id, secure_hash, is_home=False, is_index=False, is_login=False, error_message='', html='', title='', chat_id='', redirect_url='/'):
    tpath = ospath.join('bot', 'server', 'template')
    if is_login:
        async with aiopen(ospath.join(tpath, 'login.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Error -->", error_message if error_message else '').replace("<!-- Theme -->", Telegram.THEME).replace("<!-- RedirectURL -->", redirect_url)
    elif is_home:
        async with aiopen(ospath.join(tpath, 'home.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Print -->", html).replace("<!-- Theme -->", Telegram.THEME)
    elif is_index:
        async with aiopen(ospath.join(tpath, 'index.html'), 'r') as f:
            html = (await f.read()).replace("<!-- Print -->", html).replace("<!-- Theme -->", Telegram.THEME).replace("<!-- Title -->", title).replace("<!-- Chat_id -->", chat_id)
    else:
        file_data = await get_file_ids(StreamBot, chat_id=int(chat_id), message_id=int(message_id))
        if file_data.unique_id[:6] != secure_hash:
            LOGGER.info('Link hash: %s - %s', secure_hash, file_data.unique_id[:6])
            LOGGER.info('Invalid hash for message with - ID %s', message_id)
            raise InvalidHash
        filename, tag, size = file_data.file_name, file_data.mime_type.split('/')[0].strip(), get_readable_file_size(file_data.file_size)
        if tag == 'video':
            async with aiopen(ospath.join(tpath, 'video.html')) as r:
                poster = f"/api/thumb/{chat_id}?id={message_id}"
                html = (await r.read()).replace('<!-- Filename -->', filename).replace("<!-- Theme -->", Telegram.THEME).replace('<!-- Poster -->', poster).replace('<!-- Size -->', size)
        else:
            async with aiopen(ospath.join(tpath, 'dl.html')) as r:
                html = (await r.read()).replace('<!-- Filename -->', filename).replace("<!-- Theme -->", Telegram.THEME).replace('<!-- Size -->', size)
    return html
