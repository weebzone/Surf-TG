from pymongo import DESCENDING, MongoClient
from bson import ObjectId
from bot.config import Telegram


class Database:
    def __init__(self):
        MONGODB_URI = Telegram.DATABASE_URL
        self.mongo_client = MongoClient(MONGODB_URI)
        self.db = self.mongo_client["surftg"]
        self.collection = self.db["playlist"]
        self.channel = self.db["channel"]
        self.files = self.db["files"]

    async def create_folder(self, parent_id, folder_name, thumbnail):
        folder = {"parent_folder": parent_id, "name": folder_name,
                  "thumbnail": thumbnail, "type": "folder"}
        self.collection.insert_one(folder)

    def delete(self, document_id):
        try:
            has_child_documents = self.collection.count_documents(
                {'parent_folder': document_id}) > 0
            if has_child_documents:
                result = self.collection.delete_many(
                    {'parent_folder': document_id})
            result = self.collection.delete_one({'_id': ObjectId(document_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f'An error occurred: {e}')
            return False

    async def edit(self, id, name, thumbnail):
        result = self.collection.update_one({"_id": ObjectId(id)}, {
            "$set": {"name": name, "thumbnail": thumbnail}})
        return result.modified_count > 0

    async def search_DbFolder(self, query):
        words = query.split()
        regex_query = {'$regex': '.*' +
                       '.*'.join(words) + '.*', '$options': 'i'}
        myquery = {'type': 'folder', 'name': regex_query}
        mydoc = self.collection.find(myquery).sort('_id', DESCENDING)
        return [{'_id': str(x['_id']), 'name': x['name']} for x in mydoc]

    async def add_json(self, data):
        result = self.collection.insert_many(data)

    async def get_Dbfolder(self, parent_id="root", page=1, per_page=50):
        query = {"parent_folder": parent_id, "type": "folder"} if parent_id != 'root' else {
            "parent_folder": 'root', "type": "folder"}
        if parent_id != 'root':
            offset = (int(page) - 1) * per_page
            return list(self.collection.find(query).skip(offset).limit(per_page))
        else:
            return list(self.collection.find(query))

    async def get_dbFiles(self, parent_id=None, page=1, per_page=50):
        query = {"parent_folder": parent_id, "type": "file"}
        offset = (int(page) - 1) * per_page
        return list(self.collection.find(query).sort(
            '_id', DESCENDING).skip(offset).limit(per_page))

    async def get_info(self, id):
        query = {'_id': ObjectId(id)}
        if document := self.collection.find_one(query):
            return document.get('name', None)
        else:
            return None

    async def search_dbfiles(self, id, query, page=1, per_page=50):
        words = query.split()
        regex_query = {'$regex': '.*' +
                       '.*'.join(words) + '.*', '$options': 'i'}
        query = {'type': 'file', 'parent_folder': id, 'name': regex_query}
        offset = (int(page) - 1) * per_page
        mydoc = self.collection.find(query).sort(
            '_id', DESCENDING).skip(offset).limit(per_page)
        return list(mydoc)

    async def get_dbchannel(self, chat_id, last_message_id):
        if existing_entry := self.channel.find_one({"chat_id": chat_id}):
            first_message_id = existing_entry["first_message_id"]
            last_message_id = existing_entry["last_message_id"]
        else:
            self.channel.insert_one(
                {"chat_id": chat_id, "last_message_id": last_message_id, "first_message_id": 1})
            first_message_id = 1
        return {"chat_id": chat_id, "first_message_id": first_message_id, "last_message_id": last_message_id}


    async def get_dbchannel_update(self, chat_id, last_message_id):
            self.channel.update_one(
                {"chat_id": chat_id},
                {"$set": {"first_message_id": last_message_id, "last_message_id": last_message_id}}
            )


    async def add_files(self, data):
        result = self.files.insert_many(data)

    async def list_tgfiles(self, id, page=1, per_page=50):
        query = {'chat_id': id}
        offset = (int(page) - 1) * per_page
        mydoc = self.files.find(query).sort(
            'msg_id', DESCENDING).skip(offset).limit(per_page)
        return list(mydoc)

    async def search_tgfiles(self, id, query, page=1, per_page=50):
        words = query.split()
        regex_query = {'$regex': '.*' +
                       '.*'.join(words) + '.*', '$options': 'i'}
        query = {'chat_id': id, 'title': regex_query}
        offset = (int(page) - 1) * per_page
        mydoc = self.files.find(query).sort(
            'msg_id', DESCENDING).skip(offset).limit(per_page)
        return list(mydoc)


    def delete_file(self, chat_id, msg_id, hash):
        try:
            result = self.files.delete_one({'chat_id': str(chat_id), 'msg_id': int(msg_id), 'hash': str(hash)})
            return result.deleted_count > 0
        except Exception as e:
            print(f'An error occurred: {e}')
            return False