import os
from pyrogram import Client, filters
from pyrogram.types import Message
from . import *
from . import HelpMenu, custom_handler, on_message

# Define a custom filter if needed (example for disappearing messages)
def self_destruction_filter(_, __, message: Message):
    return (
        hasattr(message, "ttl_seconds") and message.ttl_seconds is not None
    )

# Register the filter in pyrogram.filters (if it needs to be dynamic)
filters.self_destruction = filters.create(self_destruction_filter)

@custom_handler(filters.self_destruction, group=-6)
async def save_timer_media(client: Client, message: Message):
    try:
        if message.media:
            file_path = await message.download()
            await client.send_document(
                "me",
                document=file_path,
                caption=message.caption or "Saved timer media"
            )
            os.remove(file_path)
    except Exception as e:
        print(f"Error: {e}")
