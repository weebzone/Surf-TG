from asyncio import gather, create_task
from bot.helper.database import Database
from bot.telegram import StreamBot
from bot.config import Telegram

db = Database()

async def get_chats():
    AUTH_CHANNEL = await db.get_variable('auth_channel')
    if AUTH_CHANNEL is None or AUTH_CHANNEL.strip() == '':
        AUTH_CHANNEL = Telegram.AUTH_CHANNEL
    else:
        AUTH_CHANNEL = [channel.strip() for channel in AUTH_CHANNEL.split(",")]
    
    return [{"chat-id": chat.id, "title": chat.title or chat.first_name, "type": chat.type.name} for chat in await gather(*[create_task(StreamBot.get_chat(int(channel_id))) for channel_id in AUTH_CHANNEL])]


async def posts_chat(channels):
    phtml = """
            <div class="col channel-card">
                <a href="/channel/{cid}">
                    <div class="card profile-card text-white bg-primary mb-2">
                    
                        <div class="img-container text-center"
                            style="width: 145px; height: 145px; display: inline-block; overflow: hidden; position: relative; border-radius: 50%; margin: auto;">
                            <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif" class="card-img-top lzy_img"
                                data-src="{img}" alt="{title}"
                                style="object-fit: cover; width: 100%; height: 100%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                        </div>
            
                        <div class="card-body p-1 text-center">
                            <div>
                                <h6 class="card-title">{title}</h6>
                                <span class="badge bg-warning">{ctype}</span>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
"""
    return ''.join(phtml.format(cid=str(channel["chat-id"]).replace("-100", ""), img=f"/api/thumb/{channel['chat-id']}", title=channel["title"], ctype=channel['type']) for channel in channels)


async def post_playlist(playlists):
    dhtml = """
    <div class="col">

        <div class="card profile-card text-white bg-primary mb-2">
            <a href="" onclick="openEditPopupForm(event, '{img}', '{ctype}', '{cid}', '{title}')"
                class="admin-only position-absolute top-0 end-0 m-2" data-bs-toggle="modal" data-bs-target="#editFolderModal"
                style="z-index: 1;"><i class="bi bi-pencil-square"></i>
            </a>
            
                <div class="img-container text-center"
                    style="width: 145px; height: 145px; display: inline-block; overflow: hidden; position: relative; border-radius: 50%; margin: auto;">
                    <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif"
                        class="card-img-top lzy_img" data-src="{img}" alt="{title}"
                        style="object-fit: cover; width: 100%; height: 100%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                </div>
            <a href="/playlist?db={cid}" style="text-align: center;">
                <div class="card-body p-1 text-center">
                    <div>
                        <h6 class="card-title">{title}</h6>
                        <span class="badge bg-warning">Folder</span>
                    </div>
                </div>
            </a>
        </div>

    </div>
    """

    return ''.join(dhtml.format(cid=playlist["_id"], img=playlist["thumbnail"], title=playlist["name"], ctype=playlist['parent_folder']) for playlist in playlists)


async def posts_db_file(posts):
    phtml = """
    <div class="col">

        <div class="card text-white bg-primary mb-2">
            <a href=""
                onclick="openPostEditPopupForm(event, '{img}', '{type}', '{size}', '{title}', '{cid}', '{ctype}')"
                class="admin-only position-absolute top-0 end-0 m-2" data-bs-toggle="modal" data-bs-target="#editModal"><i
                    class="bi bi-pencil-square"></i></a>
            
                <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif" data-src="{img}"
                    class="card-img-top rounded-top lzy_img" alt="{title}">
                <a href="/watch/{chat_id}?id={id}&hash={hash}">
                <div class="card-body p-1">
                    <h6 class="card-title">{title}</h6>
                    <span class="badge bg-warning">{type}</span>
                    <span class="badge bg-info">{size}</span>
                </div>
                </a>
            
        </div>

    </div>
"""
    return ''.join(phtml.format(cid=post["_id"], chat_id=str(post["chat_id"]).replace("-100", ""), id=post["file_id"], img=post["thumbnail"], title=post["name"], hash=post["hash"], size=post['size'], type=post['file_type'], ctype=post["parent_folder"]) for post in posts)
