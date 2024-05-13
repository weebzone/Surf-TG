from dotenv import dotenv_values
from os import environ
from pymongo import DESCENDING, MongoClient
from bson import ObjectId
from bot.config import Telegram


class Database:
    def __init__(self):
        MONGODB_URI = Telegram.DATABASE_URL
        self.mongo_client = MongoClient(MONGODB_URI)
        self.db = self.mongo_client["surftg"]
        self.collection = self.db["playlist"]

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
    
    async def setup_config(self):
        bot_id = Telegram.BOT_TOKEN.split(":", 1)[0]
        current_config = dict(dotenv_values("config.env"))

        old_config = self.db.settings.deployConfig.find_one({"_id": bot_id})
        if old_config is None:
            self.db.settings.deployConfig.replace_one(
                {"_id": bot_id}, current_config, upsert=True
            )
        else:
            del old_config["_id"]
            if old_config != current_config:
                self.db.settings.deployConfig.replace_one(
                    {"_id": bot_id}, current_config, upsert=True
                )
        return True



    async def get_variable(self, key):
        bot_id = Telegram.BOT_TOKEN.split(":", 1)[0]
        config = self.db.settings.deployConfig.find_one({"_id": bot_id})
        return config.get(key)
        
    async def update_config(self, key, value):
        bot_id = Telegram.BOT_TOKEN.split(":", 1)[0]
        update_result = self.db.settings.deployConfig.update_one(
            {"_id": bot_id},
            {"$set": {key: value}}
        )
        if update_result.modified_count > 0:
            environ[key] = str(value)
            return True
        return False