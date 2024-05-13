from time import time
from dotenv import dotenv_values, load_dotenv
from logging import getLogger, FileHandler, StreamHandler, INFO, ERROR, basicConfig
from os import getenv
from uvloop import install
from pymongo import MongoClient

install()
load_dotenv("config.env", override=True)
basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

getLogger("aiohttp").setLevel(ERROR)
getLogger("pyrogram").setLevel(ERROR)
getLogger("aiohttp.web").setLevel(ERROR)

LOGGER = getLogger(__name__)
StartTime = time()

__version__ = "1.2.4"

bot_id = getenv('BOT_TOKEN').split(":", 1)[0]
database_url = getenv('DATABASE_URL')

if database_url:
    conn = MongoClient(database_url)
    db = conn.surftg
    current_config = dotenv_values("config.env")
    old_config = db.settings.deployConfig.find_one({"_id": bot_id})

    if old_config is None:
        db.settings.deployConfig.replace_one(
            {"_id": bot_id}, current_config, upsert=True)
    else:
        del old_config["_id"]
        if old_config != current_config:
            db.settings.deployConfig.replace_one(
                {"_id": bot_id}, current_config, upsert=True
            )