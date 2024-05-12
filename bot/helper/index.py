import json
from os.path import splitext
from bot.helper.database import Database
from bot.telegram import StreamBot
from bot.helper.file_size import get_readable_file_size

db = Database()

message_cache = {}

async def get_messages(chat_id, first_message_id, last_message_id):
    messages = []
    current_message_id = first_message_id
    while current_message_id <= last_message_id:
        if current_message_id in message_cache:
            message = message_cache[current_message_id]
        else:
            try:
                message = await StreamBot.get_messages(chat_id, current_message_id)
                message_cache[current_message_id] = message
            except Exception as e:
                break

        file = message.video or message.document
        if not file:
            current_message_id += 1
            continue
        title = file.file_name or message.caption or file.file_id
        title, _ = splitext(title)
        title = title.replace('.', ' ').replace('|', ' ').replace('_', ' ')
        messages.append({"msg_id": message.id, "title": title,
                         "hash": file.file_unique_id[:6], "size": get_readable_file_size(file.file_size), "type": file.mime_type, "chat_id": str(chat_id)})
        current_message_id += 1
    return messages


async def get_files(chat_id, page=1):
    try:
        msg = await StreamBot.send_message(int(chat_id), "Message sent By **Surf-TG**!", disable_notification=True)
        last_id = msg.id
        await msg.delete()
        data = await db.get_dbchannel(chat_id, last_id)
        if last_id != data['first_message_id']:
            fmsg_id = data['first_message_id']
            get = await get_messages(int(chat_id), int(fmsg_id), int(last_id))
            json_data = json.dumps(get)
            if data := json.loads(json_data):
                await db.add_files(data)
        return await db.list_tgfiles(id=chat_id, page=page)
    except Exception as e:
        print(e)


async def posts_file(posts, chat_id):
    phtml = """
            <div class="col">
                
                    <div class="card text-white bg-primary mb-3">
                        <input type="checkbox" class="admin-only form-check-input position-absolute top-0 end-0 m-2"
                            onchange="checkSendButton()" id="selectCheckbox"
                            data-id="{id}|{hash}|{title}|{size}|{type}|{img}">
                        <img src="https://cdn.jsdelivr.net/gh/weebzone/weebzone/data/Surf-TG/src/loading.gif" class="lzy_img card-img-top rounded-top"
                            data-src="{img}" alt="{title}">
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
    return ''.join(phtml.format(chat_id=str(chat_id).replace("-100", ""), id=post["msg_id"], img=f"/api/thumb/{chat_id}?id={post['msg_id']}", title=post["title"], hash=post["hash"], size=post['size'], type=post['type']) for post in posts)
