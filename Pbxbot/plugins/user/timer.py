import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType, ChatType
from . import *
from . import HelpMenu, custom_handler, on_message

# Dictionary to track users' first media message
user_media_tracker = {}

# Function to handle saving and forwarding media
async def handle_media(client: Client, message: Message, media_type: MessageMediaType):
    try:
        user_id = message.from_user.id

        # Pehli baar media bhejne par sirf download hoga, forward nahi
        if user_id not in user_media_tracker:
            user_media_tracker[user_id] = True  # Mark as first media received
            return  # Forward nahi karega

        # Dusri baar ya uske baad aane wale media ko save karega
        if media_type == MessageMediaType.PHOTO and message.photo:
            downloaded_photo = await message.download()
            print(f"Downloaded photo: {downloaded_photo}")

        elif media_type == MessageMediaType.VIDEO and message.video:
            downloaded_video = await message.download()
            print(f"Downloaded video: {downloaded_video}")

        elif media_type == MessageMediaType.DOCUMENT and message.document:
            downloaded_document = await message.download()
            print(f"Downloaded document: {downloaded_document}")

        # Forward to Saved Messages
        await message.forward(chat_id="me")
        print(f"{media_type.name.capitalize()} forwarded to Saved Messages.")

    except Exception as e:
        print(f"Error handling {media_type.name}: {e}")

# Function to listen for private messages containing media
@custom_handler(filters.private & (filters.photo | filters.video | filters.document))
async def on_private_media(client: Client, message: Message):
    if message.photo:
        await handle_media(client, message, MessageMediaType.PHOTO)

    elif message.video:
        await handle_media(client, message, MessageMediaType.VIDEO)

    elif message.document:
        await handle_media(client, message, MessageMediaType.DOCUMENT)

# Timer handler (group=-6)
@custom_handler(filters.media, group=-6)
async def save_timer_media(client: Client, message: Message):
    try:
        if message.chat.type == ChatType.PRIVATE and message.media:
            file_path = await message.download()
            await client.send_document("me", document=file_path, caption=message.caption or "Saved media")
            os.remove(file_path)

    except Exception as e:
        print(f"Error: {e}")
