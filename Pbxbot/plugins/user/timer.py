import os
from . import *
from pyrogram import Client, filters
from Pbxbot.core import Pbxbot
from pyrogram.types import Message


@on_message(filters.self_destruction, group=6)
async def save_timer_media(Pbxbot: Pbxbot, message: Message):
    try:
        if message.media:
            file_path = await message.download()
            await Pbxbot.send_document("me", document=file_path, caption=message.caption or "Saved timer media")
            os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")
