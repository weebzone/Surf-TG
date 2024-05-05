from bot.telegram import StreamBot
from bot.config import Telegram



# Function to get channels
async def get_chats():
    channels = []
    for channel_id in Telegram.AUTH_CHANNEL:
        chat = await StreamBot.get_chat(int(channel_id))
        chat_id = chat.id
        chat_type = chat.type.name
        chat_title = chat.title or chat.first_name
        channels.append(
            {"chat-id": chat_id, "title": chat_title, "type": chat_type})
    return channels



# Function to generate HTML for channels
async def posts_chat(channels):
    html = ""
    phtml = """<div class="content">
            <a href="/channel/{id}">
                <!-- Your content here -->
                <div class="card bg-light mb-3 shadow-sm">
                <div class="img-container">
                    <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif" data-src="{img}" alt="{title}" class="img lzy_img">
                    </div><div class="card-body">
                        <p class="card-subtitle">{title}</p>
                        <span class="badge bg-info">{type}</span>
                    </div>
                </div>
            </a>
        </div>"""

    for channel in channels:
        html += phtml.format(
            id=channel["chat-id"],
            img=f"/api/thumb/{channel['chat-id']}",
            title=channel["title"],
            type=channel['type']
        )
    return html
