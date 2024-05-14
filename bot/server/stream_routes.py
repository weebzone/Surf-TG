import json
import logging
import math
import mimetypes
import secrets
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from bot.helper.chats import get_chats, post_playlist, posts_chat, posts_db_file
from bot.helper.database import Database
from bot.helper.search import search
from bot.helper.thumbnail import get_image
from bot.telegram import work_loads, multi_clients
from aiohttp_session import get_session
from bot.config import Telegram
from bot.helper.exceptions import FIleNotFound, InvalidHash
from bot.helper.index import get_files, posts_file
from bot.server.custom_dl import ByteStreamer
from bot.server.render_template import render_page
from bot.helper.cache import rm_cache

from bot.telegram import StreamBot

client_cache = {}

routes = web.RouteTableDef()
db = Database()


@routes.get('/login')
async def login_form(request):
    session = await get_session(request)
    redirect_url = session.get('redirect_url', '/')
    return web.Response(text=await render_page(None, None, route='login', redirect_url=redirect_url), content_type='text/html')


@routes.post('/login')
async def login_route(request):
    session = await get_session(request)
    if 'user' in session:
        return web.HTTPFound('/')
    data = await request.post()
    username = data.get('username')
    password = data.get('password')
    error_message = None
    if (username == Telegram.USERNAME and password == Telegram.PASSWORD) or (username == Telegram.ADMIN_USERNAME and password == Telegram.ADMIN_PASSWORD):
        session['user'] = username
        if 'redirect_url' not in session:
            session['redirect_url'] = '/'
        redirect_url = session['redirect_url']
        del session['redirect_url']
        return web.HTTPFound(redirect_url)
    else:
        error_message = "Invalid username or password"
    return web.Response(text=await render_page(None, None, route='login', msg=error_message), content_type='text/html')


@routes.post('/logout')
async def logout_route(request):
    session = await get_session(request)
    session.pop('user', None)
    return web.HTTPFound('/login')


@routes.post('/create')
async def create_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})
    data = await request.post()
    folderName = data.get('folderName')
    thumbnail = data.get('thumbnail')
    parent_dir = data.get('parent_dir')
    parent_dir = parent_dir.split('db=')[-1] if 'db=' in parent_dir else 'root'
    await db.create_folder(parent_dir, folderName, thumbnail)
    if parent_dir == 'root':
        return web.HTTPFound('/')
    else:
        return web.HTTPFound(f'/playlist?db={parent_dir}')


@routes.post('/delete')
async def delete_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})
    data = await request.json()
    id = data.get('delete_id')
    parent = data.get('parent')
    if not (success := db.delete(id)):
        return web.HTTPInternalServerError()
    if parent == 'root':
        return web.HTTPFound('/')
    else:
        return web.HTTPFound(f'/playlist?db={parent}')


@routes.post('/edit')
async def editFolder_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})
    data = await request.post()
    folderName = data.get('folderName')
    thumbnail = data.get('thumbnail')
    id = data.get('folder_id')
    parent = data.get('parent')
    success = await db.edit(id, folderName, thumbnail)
    if not success:
        return web.HTTPInternalServerError()
    if parent == 'root':
        return web.HTTPFound('/')
    else:
        return web.HTTPFound(f'/playlist?db={parent}')


@routes.post('/edit_post')
async def editPost_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})
    data = await request.post()
    fileName = data.get('fileName')
    thumbnail = data.get('filethumbnail')
    id = data.get('file_id')
    parent = data.get('file_folder_id')
    success = await db.edit(id, fileName, thumbnail)
    if not success:
        return web.HTTPInternalServerError()
    if parent == 'root':
        return web.HTTPFound('/')
    else:
        return web.HTTPFound(f'/playlist?db={parent}')


@routes.get('/searchDbFol')
async def searchDbFolder_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})
    query = request.query.get('query', '')
    folder_names = await db.search_DbFolder(query)
    return web.json_response(folder_names)


@routes.post('/send')
async def send_route(request):
    data = await request.post()
    chat_id = data.get('chatId')
    chat_id = f"-100{chat_id}"
    folder_id = data.get('folderId')
    selected_ids = data.get('selectedIds')
    if not all([chat_id, folder_id, selected_ids]):
        return {'error': 'Missing required data in request'}

    formatted_entries = []
    for entry in selected_ids.split(','):
        file_id, hash, filename, size, file_type, thumbnail = entry.split('|')
        formatted_entries.append({
            'chat_id': chat_id,
            'parent_folder': folder_id,
            'file_id': file_id,
            'hash': hash,
            'name': filename,
            'size': size,
            'file_type': file_type,
            'thumbnail': thumbnail,
            'type': 'file'
        })

    json_data = json.dumps(formatted_entries)
    data = json.loads(json_data)
    await db.add_json(data)
    if folder_id == 'root':
        return web.HTTPFound('/')
    else:
        return web.HTTPFound(f'/playlist?db={folder_id}')


@routes.get('/reload')
async def reload_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})

    chat_id = request.query.get('chatId', '')
    if chat_id == 'home':
        rm_cache()
        return web.HTTPFound('/')
    else:
        rm_cache(f"-100{chat_id}")
        return web.HTTPFound(f'/channel/{chat_id}')


@routes.post('/config')
async def editConfig_route(request):
    session = await get_session(request)
    if (username := session.get('user')) != Telegram.ADMIN_USERNAME:
        return web.json_response({'msg': 'Who the hell you are'})
    data = await request.post()
    channel = data.get('channel')
    theme = data.get('theme')
    success = await db.update_config(theme=theme, auth_channel=channel)
    if not success:
        return web.HTTPInternalServerError()
    return web.HTTPFound('/')



@routes.get('/')
async def home_route(request):
    session = await get_session(request)
    if username := session.get('user'):
        try:
            channels = await get_chats()
            playlists = await db.get_Dbfolder()
            phtml = await posts_chat(channels)
            dhtml = await post_playlist(playlists)
            is_admin = username == Telegram.ADMIN_USERNAME
            return web.Response(text=await render_page(None, None, route='home', html=phtml, playlist=dhtml, is_admin=is_admin), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e)) from e
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')


@routes.get('/playlist')
async def playlist_route(request):
    session = await get_session(request)
    if username := session.get('user'):
        try:
            parent_id = request.query.get('db')
            page = request.query.get('page', '1')
            playlists = await db.get_Dbfolder(parent_id, page=page)
            files = await db.get_dbFiles(parent_id, page=page)
            text = await db.get_info(parent_id)
            dhtml = await post_playlist(playlists)
            dphtml = await posts_db_file(files)
            is_admin = username == Telegram.ADMIN_USERNAME
            return web.Response(text=await render_page(parent_id, None, route='playlist', playlist=dhtml, database=dphtml, msg=text, is_admin=is_admin), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e)) from e
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')


@routes.get('/search/db/{parent}')
async def dbsearch_route(request):
    session = await get_session(request)
    if username := session.get('user'):
        parent = request.match_info['parent']
        page = request.query.get('page', '1')
        query = request.query.get('q')
        is_admin = username == Telegram.ADMIN_USERNAME
        try:
            files = await db.search_dbfiles(id=parent, page=page, query=query)
            dphtml = await posts_db_file(files)
            name = await db.get_info(parent)
            text = f"{name} - {query}"
            return web.Response(text=await render_page(parent, None, route='playlist', database=dphtml, msg=text, is_admin=is_admin), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e)) from e
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')


@routes.get('/channel/{chat_id}')
async def channel_route(request):
    session = await get_session(request)
    if username := session.get('user'):
        chat_id = request.match_info['chat_id']
        chat_id = f"-100{chat_id}"
        page = request.query.get('page', '1')
        is_admin = username == Telegram.ADMIN_USERNAME
        try:
            posts = await get_files(chat_id, page=page)
            phtml = await posts_file(posts, chat_id)
            chat = await StreamBot.get_chat(int(chat_id))
            return web.Response(text=await render_page(None, None, route='index', html=phtml, msg=chat.title, chat_id=chat_id.replace("-100", ""), is_admin=is_admin), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e)) from e
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')


@routes.get('/search/{chat_id}')
async def search_route(request):
    session = await get_session(request)
    if username := session.get('user'):
        chat_id = request.match_info['chat_id']
        chat_id = f"-100{chat_id}"
        page = request.query.get('page', '1')
        query = request.query.get('q')
        is_admin = username == Telegram.ADMIN_USERNAME
        try:
            posts = await search(chat_id, page=page, query=query)
            phtml = await posts_file(posts, chat_id)
            chat = await StreamBot.get_chat(int(chat_id))
            text = f"{chat.title} - {query}"
            return web.Response(text=await render_page(None, None, route='index', html=phtml, msg=text, chat_id=chat_id.replace("-100", ""), is_admin=is_admin), content_type='text/html')
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e)) from e
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')


@routes.get('/api/thumb/{chat_id}', allow_head=True)
async def get_thumbnail(request):
    chat_id = request.match_info['chat_id']
    if message_id := request.query.get('id'):
        img = await get_image(chat_id, message_id)
    else:
        img = await get_image(chat_id, None)
    response = web.FileResponse(img)
    response.content_type = "image/jpeg"
    return response


@routes.get('/watch/{chat_id}', allow_head=True)
async def stream_handler_watch(request: web.Request):
    session = await get_session(request)
    if username := session.get('user'):
        try:
            chat_id = request.match_info['chat_id']
            chat_id = f"-100{chat_id}"
            message_id = request.query.get('id')
            secure_hash = request.query.get('hash')
            return web.Response(text=await render_page(message_id, secure_hash, chat_id=chat_id), content_type='text/html')
        except InvalidHash as e:
            raise web.HTTPForbidden(text=e.message) from e
        except FIleNotFound as e:
            db.delete_file(chat_id=chat_id, msg_id=message_id, hash=secure_hash)
            raise web.HTTPNotFound(text=e.message) from e
        except (AttributeError, BadStatusLine, ConnectionResetError):
            pass
        except Exception as e:
            logging.critical(e.with_traceback(None))
            raise web.HTTPInternalServerError(text=str(e)) from e
    else:
        session['redirect_url'] = request.path_qs
        return web.HTTPFound('/login')


@routes.get('/{chat_id}/{encoded_name}', allow_head=True)
async def stream_handler(request: web.Request):
    try:
        chat_id = request.match_info['chat_id']
        chat_id = f"-100{chat_id}"
        message_id = request.query.get('id')
        name = request.match_info['encoded_name']
        secure_hash = request.query.get('hash')
        return await media_streamer(request, int(chat_id), int(message_id), secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message) from e
    except FIleNotFound as e:
        db.delete_file(chat_id=chat_id, msg_id=message_id, hash=secure_hash)
        raise web.HTTPNotFound(text=e.message) from e
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
