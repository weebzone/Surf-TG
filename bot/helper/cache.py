import os
import json

from bot import LOGGER

def rm_cache(channel=None):
    LOGGER.info("Cleaning Cache...")
    try:
        for file in os.listdir("cache"):
            try:
                if file.endswith(".json") and (channel and file.startswith(channel) or not channel):
                    os.remove(f"cache/{file}")
                    LOGGER.info(f"Removed {file}")
            except Exception as e:
                LOGGER.error(e)
    except Exception as e:
        LOGGER.error(e)


def get_cache(channel, page):
    if os.path.exists(f"cache/{channel}-{page}.json"):
        with open(f"cache/{channel}-{page}.json", "r") as f:
            return json.load(f)["posts"]
    else:
        return None


def save_cache(channel, cache, page):
    with open(f"cache/{channel}-{page}.json", "w") as f:
        json.dump(cache, f)