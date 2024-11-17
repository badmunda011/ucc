import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

OWNER_ID = int(getenv("OWNER_ID", "7009601543"))

SUKH = getenv("SUKH", "mongodb+srv://Badmunda_13:badmunda50@cluster0.9oyzqux.mongodb.net/?retryWrites=true&w=majority")
