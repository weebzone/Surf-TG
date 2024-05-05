import logging
import math
import mimetypes
import secrets
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from bot.helper.chats import get_chats, posts_chat
from bot.helper.search import search
from bot.helper.thumbnail import get_image
from bot.telegram import work_loads, multi_clients
from aiohttp_session import get_session
from bot.config import Telegram
from bot.helper.exceptions import FIleNotFound, InvalidHash
from bot.helper.index import get_files, posts_file
from bot.server.custom_dl import ByteStreamer
from bot.server.render_template import render_page
from os import path as ospath

from bot.telegram import StreamBot

client_cache = {}

routes = web.RouteTableDef()


@routes.get('/login')
async def login_form(request):
    session = await get_session(request)
    redirect_url = session.get('redirect_url', '/')
    return web.Response(text=await render_page(None, None, is_login=True, redirect_url=redirect_url), content_type='text/html')


@routes.post('/login')
async def login(request):
    session = await get_session(request)
    if 'user' in session:
        return web.HTTPFound('/')
    data = await request.post()
    username = data.get('username')
    password = data.get('password')
    error_message = None
    if username == Telegram.USERNAME and password == Telegram.PASSWORD:
        session['user'] = username
        if 'redirect_url' not in session:
            session['redirect_url'] = '/'
        redirect_url = session['redirect_url']
        del session['redirect_url']
        return web.HTTPFound(redirect_url)
    else:
        error_message = "Invalid username or password"
    return web.Response(text=await render_page(None, None, is_login=True, error_message=error_message), content_type='text/html')


@routes.post('/logout')
async def logout(request):
    session = await get_session(request)
    session.pop('user', None)
    if 'redirect_url' in session:
        del session['redirect_url']
    return web.HTTPFound('/login')

@routes.get('/')
async def home_route_handler(request):
    session = await get_session(request)
    username = session.get('user')
    if username:
        try:
            channels = await get_chats()
            phtml = await posts_chat(channels)
            return web.Response(text=await render_page(None, None, is_home=True, html=phtml), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e))
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')

@routes.get('/channel/{chat_id}')
async def channel_route_handler(request):
    session = await get_session(request)
    username = session.get('user')
    if username:
        chat_id = request.match_info['chat_id']
        page = request.query.get('page', '1')
        try:
            posts = await get_files(chat_id, page=page)
            phtml = await posts_file(posts, chat_id)
            chat = await StreamBot.get_chat(int(chat_id))
            return web.Response(text=await render_page(None, None, is_index=True, html=phtml, title=chat.title, chat_id=chat_id), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e))
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')

@routes.get('/search/{chat_id}')
async def handle_search(request):
    session = await get_session(request)
    username = session.get('user')
    if username:
        chat_id = request.match_info['chat_id']
        page = request.query.get('page', '1')
        query = request.query.get('q')
        try:
            posts = await search(chat_id, page=page, query=query)
            phtml = await posts_file(posts, chat_id)
            chat = await StreamBot.get_chat(int(chat_id))
            text = f"{chat.title} - {query}"
            return web.Response(text=await render_page(None, None, is_index=True, html=phtml, title=text, chat_id=chat_id), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e))
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')

@routes.get('/api/thumb/{chat_id}', allow_head=True)
async def get_thumbnail(request):
    chat_id = request.match_info['chat_id']
    message_id = request.query.get('id')
    if message_id:
        img = await get_image(chat_id, message_id)
    else:
        img = await get_image(chat_id, None)
    response = web.FileResponse(img)
    response.content_type = "image/jpeg"
    return response

@routes.get('/watch/{chat_id}', allow_head=True)
async def stream_handler_watch(request: web.Request):
    session = await get_session(request)
    username = session.get('user')
    if username:
        try:
            chat_id = request.match_info['chat_id']
            message_id = request.query.get('id')
            secure_hash = request.query.get('hash')
            return web.Response(text=await render_page(message_id, secure_hash, chat_id=chat_id), content_type='text/html')
        except InvalidHash as e:
            raise web.HTTPForbidden(text=e.message)
        except FIleNotFound as e:
            raise web.HTTPNotFound(text=e.message)
        except (AttributeError, BadStatusLine, ConnectionResetError):
            pass
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e))
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')

@routes.get('/{chat_id}', allow_head=True)
async def stream_handler(request: web.Request):
    try:
        chat_id = request.match_info['chat_id']
        message_id = request.query.get('id')
        secure_hash = request.query.get('hash')
        return await media_streamer(request, int(chat_id), int(message_id), secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(e.with_traceback(None))
        raise web.HTTPInternalServerError(text=str(e))


class_cache = {}

async def media_streamer(request: web.Request, chat_id: int, id: int, secure_hash: str):
    range_header = request.headers.get("Range", 0)

    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]

    if Telegram.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(chat_id=chat_id, message_id=id)
    logging.debug("after calling get_file_properties")

    if file_id.unique_id[:6] != secure_hash:
        logging.debug(f"Invalid hash for message with ID {id}")
        raise InvalidHash

    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - \
        math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if mime_type:
        if not file_name:
            try:
                file_name = f"{secrets.token_hex(2)}.{mime_type.split('/')[1]}"
            except (IndexError, AttributeError):
                file_name = f"{secrets.token_hex(2)}.unknown"
    else:
        if file_name:
            mime_type = mimetypes.guess_type(file_id.file_name)
        else:
            mime_type = "application/octet-stream"
            file_name = f"{secrets.token_hex(2)}.unknown"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
