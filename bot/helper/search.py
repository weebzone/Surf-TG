from bot.telegram import UserBot
from pyrogram.types import Message
from bot.helper.file_size import get_readable_file_size


async def search(chat_id, query, page):
    posts = []
    async for post in UserBot.search_messages(chat_id=int(chat_id), limit=50, query=str(query), offset=(int(page) -1 ) * 50):
        post: Message
        if post.video:
            file = post.video
        elif post.document:
            file = post.document
        else:
            continue
        file_name = file.file_name or post.caption or file.file_id
        file_name = file_name[:200]
        hash = file.file_unique_id[:6]
        title = " ".join(file_name.split(".")[:-1])
        size = get_readable_file_size(file.file_size)
        type = file.mime_type
        posts.append({"msg_id": post.id, "title": title,
                     "hash": hash, "size": size, "type": type})
    return posts

