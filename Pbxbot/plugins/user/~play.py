from asyncio.queues import QueueEmpty
from pyrogram import filters
from pytgcalls.exceptions import GroupCallNotFound
from pyrogram import Client, filters

from . import *
from Pbxbot.bad.streamtype import *
from Pbxbot.bad.utilities import queues

# Function to handle downloading media with cookie support
async def download_media_with_cookies(client, message, cookies=None):
    file = None
    if message.reply_to_message:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            file = await client.download_media(message.reply_to_message, cookies=cookies)
        elif message.reply_to_message.video or message.reply_to_message.document:
            file = await client.download_media(message.reply_to_message, cookies=cookies)
    return file

# Audio Player
@Client.on_message(filters.command("play") & filters.private)
async def audio_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing ...**")
    cookies = "Pbxbot/cookies.txt"  # Specify the path to your cookies file if needed
    audio = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message
        else None
    )
    type = "Audio"
    try:
        if audio:
            await aux.edit("Downloading ...")
            file = await download_media_with_cookies(client, message, cookies)
        else:
            if len(message.command) < 2:
                return await aux.edit("**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**")
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            link = results[0]
            file = await get_stream(link, type, cookies)
        
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("Playing!")
            elif a.status in ["playing", "paused"]:
                position = await queues.put(chat_id, file=file, type=type)
                await aux.edit(f"Queued At {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("Playing!")
    except Exception as e:
        print(f"Error: {e}")
        return await aux.edit("**Please Try Again !**")

# Video Player
@Client.on_message(filters.command("vplay") & filters.private)
async def video_stream(client, message):
    chat_id = message.chat.id
    aux = await eor(message, "**Processing ...**")
    cookies = "Pbxbot/cookies.txt"
    video = (
        (
            message.reply_to_message.video
            or message.reply_to_message.document
        )
        if message.reply_to_message
        else None
    )
    type = "Video"
    try:
        if video:
            await aux.edit("Downloading ...")
            file = await download_media_with_cookies(client, message, cookies)
        else:
            if len(message.command) < 2:
                return await aux.edit("**🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗...**")
            if "?si=" in message.text:
                query = message.text.split(None, 1)[1].split("?si=")[0]
            else:
                query = message.text.split(None, 1)[1]
            results = await get_result(query)
            link = results[0]
            file = await get_stream(link, type, cookies)
        
        try:
            a = await call.get_call(chat_id)
            if a.status == "not_playing":
                stream = await run_stream(file, type)
                await call.change_stream(chat_id, stream)
                await aux.edit("Playing!")
            elif a.status in ["playing", "paused"]:
                position = await queues.put(chat_id, file=file, type=type)
                await aux.edit(f"Queued At {position}")
        except GroupCallNotFound:
            stream = await run_stream(file, type)
            await call.join_group_call(chat_id, stream)
            await aux.edit("Playing!")
    except Exception as e:
        print(f"Error: {e}")
        return await aux.edit("**Please Try Again !**")
