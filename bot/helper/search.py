from bot.telegram import UserBot
from bot.helper.file_size import get_readable_file_size

async def search(chat_id, query, page):
    posts = []
    async for post in UserBot.search_messages(chat_id=int(chat_id), limit=50, query=str(query), offset=(int(page) -1 ) * 50):
        file = post.video or post.document
        if not file:
            continue
        title = " ".join((file.file_name or post.caption or file.file_id)[:200].split(".")[:-1])
        posts.append({"msg_id": post.id, "title": title,
                     "hash": file.file_unique_id[:6], "size": get_readable_file_size(file.file_size), "type": file.mime_type})
    return posts

