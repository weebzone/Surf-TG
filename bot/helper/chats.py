from asyncio import gather, create_task
from bot.telegram import StreamBot
from bot.config import Telegram

async def get_chats():
    return [{"chat-id": chat.id, "title": chat.title or chat.first_name, "type": chat.type.name} for chat in await gather(*[create_task(StreamBot.get_chat(int(channel_id))) for channel_id in Telegram.AUTH_CHANNEL])]
    
async def posts_chat(channels):
    phtml = """<div class="content">
            <a href="/channel/{cid}">
                <div class="card bg-light mb-3 shadow-sm">
                <div class="img-container">
                    <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif" data-src="{img}" alt="{title}" class="img lzy_img">
                    </div><div class="card-body">
                        <p class="card-subtitle">{title}</p>
                        <span class="badge bg-info">{ctype}</span>
                    </div>
                </div>
            </a>
        </div>"""

    return ''.join(phtml.format(cid=channel["chat-id"], img=f"/api/thumb/{channel['chat-id']}", title=channel["title"], ctype=channel['type']) for channel in channels)
