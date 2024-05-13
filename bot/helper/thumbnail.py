from os import path as ospath
from bot import LOGGER
from bot.telegram import StreamBot

image_cache = {}
path = ospath.join('bot/server/static', 'thumbnail.jpg')

async def get_image(chat_id, message_id):
    global image_cache
    cache_key = f"{chat_id}-{message_id}" if message_id else f"{chat_id}"
    if cache_key in image_cache:
        return image_cache[cache_key]
    try:
        if message_id is None:
            chat = await StreamBot.get_chat(int(chat_id))
            img = await StreamBot.download_media(str(chat.photo.big_file_id)) if chat.photo else path
        else:
            msg = await StreamBot.get_messages(int(chat_id), int(message_id))
            img = await StreamBot.download_media(str(msg.video.thumbs[0].file_id)) if msg.video else path

        image_cache[cache_key] = img
        return img
    except Exception as e:
        LOGGER.error(f"Generate Img Error: {e}")
        return
