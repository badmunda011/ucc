import os
import time
import bad
import uvloop
from platform import python_version
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

import heroku3
from pyrogram import __version__ as pyrogram_version

from .core import LOGS, Config

START_TIME = time.time()


__version__ = {
    "Pbxbot": "3.0",
    "pyrogram": pyrogram_version,
    "python": python_version(),
}

uvloop.install()

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGS = logging.getLogger(__name__)
boot = time.time()
mongodb = MongoCli(bad.SUKH)
db = mongodb.Anonymous
mongo = MongoClient(bad.SUKH)
OWNER = bad.OWNER_ID
_boot_ = time.time()
clonedb = None
def dbb():
    global db
    global clonedb
    clonedb = {}
    db = {}

try:
    if Config.HEROKU_APIKEY is not None and Config.HEROKU_APPNAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_APIKEY).apps()[
            Config.HEROKU_APPNAME
        ]
    else:
        HEROKU_APP = None
except Exception as e:
    LOGS.error(f"Heroku Api - {e}")
    HEROKU_APP = None


if Config.API_HASH is None:
    LOGS.error("Please set your API_HASH !")
    quit(1)

if Config.API_ID == 0:
    LOGS.error("Please set your API_ID !")
    quit(1)

if Config.BOT_TOKEN is None:
    LOGS.error("Please set your BOT_TOKEN !")
    quit(1)

if Config.DATABASE_URL is None:
    LOGS.error("Please set your DATABASE_URL !")
    quit(1)

if Config.LOGGER_ID == 0:
    LOGS.error("Please set your LOGGER_ID !")
    quit(1)

if Config.OWNER_ID == 0:
    LOGS.error("Please set your OWNER_ID !")
    quit(1)

if not os.path.isdir(Config.DWL_DIR):
    os.makedirs(Config.DWL_DIR)

if not os.path.isdir(Config.TEMP_DIR):
    os.makedirs(Config.TEMP_DIR)
