from bot.telegram import StreamBot
from os import path as ospath

image_cache = {}
tpath = ospath.join('bot', 'server', 'static')
path = ospath.join(tpath, 'thumbnail.jpg')
# Function to get posts for a given chat ID
async def get_image(chat_id, message_id):
    global image_cache
    cache_key = f"{chat_id}-{message_id}" if message_id else f"{chat_id}"
    if cache_key in image_cache:
        return image_cache[cache_key]
    try:
        if message_id is None:
            chat = await StreamBot.get_chat(int(chat_id))
            if chat.photo:
                img = await StreamBot.download_media(str(chat.photo.big_file_id))
            else:
                img = path

        else:
            msg = await StreamBot.get_messages(int(chat_id), int(message_id))
            if msg.video:
                img = await StreamBot.download_media(str(msg.video.thumbs[0].file_id))
            else:
                img = path

        image_cache[cache_key] = img
        return img
    except Exception as e:
        return None
