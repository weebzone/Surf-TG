from bot.helper.database import Database
db = Database()

async def search(chat_id, query, page):
    return await db.search_tgfiles(chat_id, query, int(page))
