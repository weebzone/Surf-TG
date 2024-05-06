from time import time
from logging import getLogger, FileHandler, StreamHandler, INFO, ERROR, basicConfig

from uvloop import install

install()
basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s", # [%(filename)s:%(lineno)d]
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

getLogger("aiohttp").setLevel(ERROR)
getLogger("pyrogram").setLevel(ERROR)
getLogger("aiohttp.web").setLevel(ERROR)

LOGGER = getLogger(__name__)
StartTime = time()

__version__ = "1.0.0"


