from bot.telegram import UserBot
from pyrogram.types import Message
from bot.helper.file_size import get_readable_file_size

async def get_files(chat_id, page=1):
    posts = []
    async for post in UserBot.get_chat_history(chat_id=int(chat_id), limit=50, offset=(int(page) - 1) * 50):
        file = post.video or post.document
        if not file:
            continue
        title = " ".join((file.file_name or post.caption or file.file_id)[:200].split(".")[:-1])
        posts.append({"msg_id": post.id, "title": title,
                     "hash": file.file_unique_id[:6], "size": get_readable_file_size(file.file_size), "type": file.mime_type})
    return posts


async def posts_file(posts, chat_id):
    phtml = """<div class="content">
            <a href="/watch/{chat_id}?id={id}&hash={hash}">
                <div class="card bg-light mb-3 shadow-sm">
                    <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif" data-src="{img}" alt="{title}" class="img lzy_img">
                    <div class="card-body">
                        <p class="card-subtitle">{title}</p>
                        <span class="badge bg-info">{type}</span>
                        <span class="badge bg-warning">{size}</span>
                    </div>
                </div>
            </a>
        </div>"""
    return ''.join(phtml.format(chat_id=chat_id, id=post["msg_id"], img=f"/api/thumb/{chat_id}?id={post['msg_id']}", title=post["title"], hash=post["hash"], size=post['size'], type=post['type']) for post in posts)
