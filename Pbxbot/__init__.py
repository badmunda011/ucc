import os
import logging
from pymongo import MongoClient
import time
import bad
import uvloop
from platform import python_version
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

import heroku3
from pyrogram import __version__ as pyrogram_version

from .core import LOGS, Config
ID_CHATBOT = None
CLONE_OWNERS = {}

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

cloneownerdb = db.clone_owners

async def load_clone_owners():
    async for entry in cloneownerdb.find():
        bot_id = entry["bot_id"]
        user_id = entry["user_id"]
        CLONE_OWNERS[bot_id] = user_id

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )
async def get_clone_owner(bot_id):
    data = await cloneownerdb.find_one({"bot_id": bot_id})
    if data:
        return data["user_id"]
    return None

async def delete_clone_owner(bot_id):
    await cloneownerdb.delete_one({"bot_id": bot_id})
    CLONE_OWNERS.pop(bot_id, None)

async def save_idclonebot_owner(clone_id, user_id):
    await cloneownerdb.update_one(
        {"clone_id": clone_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None

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
