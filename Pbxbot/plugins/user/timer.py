import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType
from . import *
from . import HelpMenu, custom_handler, on_message



# Function to handle saving and forwarding media
async def handle_media(client: Client, message: Message, media_type: MessageMediaType):
    try:
        # Handle saving the media
        if media_type == MessageMediaType.PHOTO and message.photo:
            # Download the photo
            downloaded_photo = await message.download()
            print(f"Downloaded photo: {downloaded_photo}")

        elif media_type == MessageMediaType.VIDEO and message.video:
            # Download the video
            downloaded_video = await message.download()
            print(f"Downloaded video: {downloaded_video}")

        elif media_type == MessageMediaType.DOCUMENT and message.document:
            # Download the document
            downloaded_document = await message.download()
            print(f"Downloaded document: {downloaded_document}")

        # Forward the media to Saved Messages
        await message.forward(chat_id="me")
        print(f"{media_type.name.capitalize()} forwarded to Saved Messages.")
    except Exception as e:
        print(f"Error handling {media_type.name}: {e}")


# Function to listen for private messages containing media
@custom_handler(filters.private & (filters.photo | filters.video | filters.document))
async def on_private_media(client: Client, message: Message):
    # Check for the type of media and apply the appropriate action
    if message.photo:
        await handle_media(client, message, MessageMediaType.PHOTO)

    elif message.video:
        await handle_media(client, message, MessageMediaType.VIDEO)

    elif message.document:
        await handle_media(client, message, MessageMediaType.DOCUMENT)

# timer 
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

@custom_handler(filters.media, group=-6)
async def save_timer_media(client: Client, message: Message):
    try:
        # Check if the message is in a private chat
        if message.chat.type == ChatType.PRIVATE and message.media:
            # Download the media and save it
            file_path = await message.download()

            # Send the document to your saved messages
            await client.send_document("me", document=file_path, caption=message.caption or "Saved media")

            # Remove the downloaded file from the server
            os.remove(file_path)

    except Exception as e:
        print(f"Error: {e}")
