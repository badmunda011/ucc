import os
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.self_destruction, group=6)
async def save_timer_media(client: Client, message: Message):
    try:
        if message.media:
            file_path = await message.download()
            await client.send_document("me", document=file_path, caption=message.caption or "Saved timer media")
            os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")
