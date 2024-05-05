from dotenv import load_dotenv
import os

load_dotenv("config.env")

class Telegram:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SESSION_STRING = os.getenv("SESSION_STRING")
    PORT = os.getenv("PORT", "8080")
    BASE_URL = os.getenv("BASE_URL")
    AUTH_CHANNEL = os.getenv("AUTH_CHANNEL").split(", ")
    THEME = os.getenv("THEME", "flatly")
    USERNAME = os.getenv("USERNAME", "admin")
    PASSWORD = os.getenv("PASSWORD", "admin")
    SLEEP_THRESHOLD = int(os.getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(os.getenv('WORKERS', '10'))
    MULTI_CLIENT = bool(os.getenv('MULTI_CLIENT', 'False'))