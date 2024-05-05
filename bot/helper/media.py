from pyrogram.types import Message


def is_media(message: Message):
    if not message:
        return
    return message.document or message.photo or message.video or message.audio or \
        message.voice or message.video_note or message.sticker or message.animation or None
