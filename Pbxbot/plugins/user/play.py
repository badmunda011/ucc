import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap

from . import HelpMenu, group_only, handler, Pbxbot, on_message, Config
from pyrogram import Client, filters
from Pbxbot import *

from Pbxbot.core.clients import call
from Pbxbot.core.config import *
from Pbxbot.plugins.user.play import *
from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from pyrogram.raw import functions
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler

from typing import Union, List, Pattern
from pyrogram import Client, filters as pyrofl
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_

from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl


from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch



# Group Call Config
call_config = GroupCallConfig(auto_start=False)

# Memory Database
ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
ACTIVE_MEDIA_CHATS = []
QUEUE = {}

# Required Functions
def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()

async def paste_queue(content):
    loop = asyncio.get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# MongoDB Functions
chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb

# Served Chats
async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})

# Served Users
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})
    

# Function to download the YouTube thumbnail

async def download_thumbnail_with_timeout(vidid: str):
    timeout = aiohttp.ClientTimeout(total=60)  # Set total timeout to 60 seconds
    async with aiohttp.ClientSession(timeout=timeout) as session:
        links = [
            f"https://i.ytimg.com/vi/{vidid}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/sddefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg",
            Config.PLAY_IMAGE_URL,  # Fallback image if all else fails
        ]
        thumbnail = f"cache/temp_{vidid}.jpg"
        for url in links:
            async with session.get(url) as resp:
                if resp.status != 200:
                    continue
                else:
                    # Save the thumbnail image to a file
                    f = await aiofiles.open(thumbnail, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    return thumbnail
    return Config.PLAY_IMAGE_URL  # Return default image if all else fails
    
async def download_thumbnail(vidid: str):
    async with aiohttp.ClientSession() as session:
        links = [
            f"https://i.ytimg.com/vi/{vidid}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/sddefault.jpg",
            f"https://i.ytimg.com/vi/{vidid}/hqdefault.jpg",
            Config.PLAY_IMAGE_URL,  # Fallback image if all else fails
        ]
        thumbnail = f"cache/temp_{vidid}.jpg"
        for url in links:
            async with session.get(url) as resp:
                if resp.status != 200:
                    continue
                else:
                    # Save the thumbnail image to a file
                    f = await aiofiles.open(thumbnail, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                    return thumbnail
    return Config.PLAY_IMAGE_URL  # Return default image if all else fails

# Function to generate a simple thumbnail with the video image
async def create_thumbnail(results, user_id):
    if not results:
        return Config.PLAY_IMAGE_URL  # Return default image if results are empty
    
    vidid = results.get("id")  # Get video ID

    # Download the video thumbnail image
    image = await download_thumbnail(vidid)

    try:
        # Open the downloaded image (no resizing, no additional effects)
        image01 = Image.open(image)

        # Resize the image to 1280x720 (standard YouTube thumbnail size)
        image01 = image01.resize((1280, 720))

        # Save the final image
        thumbnail_path = f"cache/{vidid}_thumbnail.jpg"
        image01.save(thumbnail_path)

        return thumbnail_path

    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return Config.PLAY_IMAGE_URL  # Return default image if error occurs

async def add_active_media_chat(
    chat_id, stream_type
):
    """
    Adds chat to the respective media stream list.
    """
    if stream_type == "Audio":
        if chat_id in ACTIVE_VIDEO_CHATS:
            ACTIVE_VIDEO_CHATS.remove(chat_id)
        if chat_id not in ACTIVE_AUDIO_CHATS:
            ACTIVE_AUDIO_CHATS.append(chat_id)
    elif stream_type == "Video":
        if chat_id in ACTIVE_AUDIO_CHATS:
            ACTIVE_AUDIO_CHATS.remove(chat_id)
        if chat_id not in ACTIVE_VIDEO_CHATS:
            ACTIVE_VIDEO_CHATS.append(chat_id)
    if chat_id not in ACTIVE_MEDIA_CHATS:
        ACTIVE_MEDIA_CHATS.append(chat_id)


async def remove_active_media_chat(chat_id):
    """
    Removes chat from the active media stream list.
    """
    if chat_id in ACTIVE_AUDIO_CHATS:
        ACTIVE_AUDIO_CHATS.remove(chat_id)
    if chat_id in ACTIVE_VIDEO_CHATS:
        ACTIVE_VIDEO_CHATS.remove(chat_id)
    if chat_id in ACTIVE_MEDIA_CHATS:
        ACTIVE_MEDIA_CHATS.remove(chat_id)


# VC Player Queue (Updated for UserBot)

async def add_to_queue(
    chat_id,
    user,
    title,
    duration,
    stream_file,
    stream_type,
    vidid,  # Video ID for thumbnail generation
):
    """
    Adds the stream details to the queue.
    """
    thumbnail = await download_thumbnail(vidid)  # Get the thumbnail
    put = {
        "chat_id": chat_id,
        "user": user,
        "title": title,
        "duration": duration,
        "stream_file": stream_file,
        "stream_type": stream_type,
        "thumbnail": thumbnail if thumbnail else "default_thumbnail.jpg",  # Use a default if none
    }
    check = QUEUE.get(chat_id)
    if check:
        QUEUE[chat_id].append(put)
    else:
        QUEUE[chat_id] = []
        QUEUE[chat_id].append(put)

    return len(QUEUE[chat_id]) - 1


async def clear_queue(chat_id):
    """
    Clears the queue for the given chat ID.
    """
    check = QUEUE.get(chat_id)
    if check:
        QUEUE.pop(chat_id)
        
        
        
# Change stream & Close Stream
async def change_stream(chat_id):
    queued = QUEUE.get(chat_id)
    if queued:
        queued.pop(0)
    if not queued:
        await Pbxbot.send_message(chat_id, "✼ Nᴏ ᴍᴏʀᴇ sᴏɴɢ, Sᴏ Lᴇғᴛ \nFʀᴏᴍ Vᴏɪᴄᴇ Cʜᴀᴛ❗...")
        return await close_stream(chat_id)

    title = queued[0].get("title")
    duration = queued[0].get("duration")
    stream_file = queued[0].get("stream_file")
    stream_type = queued[0].get("stream_type")
    thumbnail = queued[0].get("thumbnail")
    
    try:
        requested_by = queued[0].get("user").mention
    except Exception:
        if queued[0].get("user").username:
            requested_by = (
                f"[{queued[0].get('user').title}](https://t.me/"
                f"{queued[0].get('user').username})"
            )
        else:
            requested_by = queued[0].get("user").title

    # Setup media stream for either Audio or Video
    if stream_type == "Audio":
        stream_media = MediaStream(
            media_path=stream_file,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
            ytdlp_parameters="--cookies cookies.txt",
        )
    elif stream_type == "Video":
        stream_media = MediaStream(
            media_path=stream_file,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
            ytdlp_parameters="--cookies cookies.txt",
        )

    await call.play(chat_id, stream_media, config=call_config)
    await add_active_media_chat(chat_id, stream_type)
    
    caption = f"""ꜱᴛᴀʀᴛᴇᴅ ꜱᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠᴄ.
    
💫 Tɪᴛʟᴇ ❤️  {title}
🗡️ Dᴜʀᴀᴛɪᴏɴ ⏰  {duration}
🔉 Sᴛʀᴇᴀᴍ Tʏᴘᴇ 🔊  {stream_type}
💌 Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ 💌  {requested_by}"""
    
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🗑️ ᴄʟᴏꜱᴇ",
                    callback_data="force_close",
                )
            ],
        ]
    )
    return await Pbxbot.send_photo(chat_id, thumbnail, caption, reply_markup=buttons)

# Close Stream
async def close_stream(chat_id):
    try:
        await call.leave_call(chat_id)
    except Exception:
        pass
    await clear_queue(chat_id)
    await remove_active_media_chat(chat_id)

# Get Call Status
async def get_call_status(chat_id):
    calls = await call.calls
    chat_call = calls.get(chat_id)
    if chat_call:
        status = chat_call.capture
        if status == Call.Status.IDLE:
            call_status = "IDLE"
        elif status == Call.Status.ACTIVE:
            call_status = "PLAYING"
        elif status == Call.Status.PAUSED:
            call_status = "PAUSED"
    else:
        call_status = "NOTHING"

    return call_status
    
@on_message(
    "play",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def stream_audio_or_video(Pbxbot, message):
    try:
        await message.delete()
    except Exception:
        pass
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    user = message.from_user if message.from_user else message.sender_chat
    replied = message.reply_to_message
    audio = (replied.audio or replied.voice) if replied else None
    video = (replied.video or replied.document) if replied else None
    text = [
        "🥀 ᴘʀᴏᴄᴇꜱꜱɪɴɢ Qᴜᴇʀʏ... ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ! 🔄",
    ]
    aux = await message.reply_text(random.choice(text))
    if audio:
        title = "Unsupported Title"
        duration = "Unknown"
        try:
            stream_file = await replied.download()
        except Exception:
            return
        result_x = None
        stream_type = "Audio"

    elif video:
        title = "Unsupported Title"
        duration = "Unknown"
        try:
            stream_file = await replied.download()
        except Exception:
            return
        result_x = None
        stream_type = "Video"

    else:
        if len(message.command) < 2:
            return await aux.edit_text(
                "🥀 ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ǫᴜᴇʀʏ ᴛᴏ\nᴘʟᴀʏ ᴍᴜsɪᴄ ᴏʀ ᴠɪᴅᴇᴏ❗..."
            )
        query = message.text.split(None, 1)[1]
        if "https://" in query:
            base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
            resu = re.findall(base, query)
            vidid = resu[0] if resu[0] else None
        else:
            vidid = None
        url = f"https://www.youtube.com/watch?v={vidid}" if vidid else None
        search_query = url if url else query
        results = VideosSearch(search_query, limit=1)
        for result in (await results.next())["result"]:
            vid_id = vidid if vidid else result["id"]
            vid_url = url if url else result["link"]
            try:
                title = "[" + (result["title"][:18]) + "]" + f"({vid_url})"
                title_x = result["title"]
            except Exception:
                title = "Unsupported Title"
                title_x = title
            try:
                durationx = result.get("duration")
                if not durationx:
                    duration = "Live Stream"
                    duration_x = "Live"
                elif len(durationx) == 4 or len(durationx) == 7:
                    duration = f"0{durationx} Mins"
                    duration_x = f"0{durationx}"
                else:
                    duration = f"{durationx} Mins"
                    duration_x = f"{duration}"
            except Exception:
                duration = "Unknown"
                duration_x = "Unknown Mins"
            try:
                views = result["viewCount"]["short"]
            except Exception:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except Exception:
                channel = "Unknown Channel"
        stream_file = url if url else result["link"]
        result_x = {
            "title": title_x,
            "id": vid_id,
            "link": vid_url,
            "duration": duration_x,
            "views": views,
            "channel": channel,
        }
        stream_type = "Audio" if str(message.command[0][0]) != "v" else "Video"

    try:
        requested_by = user.mention
    except Exception:
        if user.username:
            requested_by = "[" + user.title + "](https://t.me/" + user.username + ")"
        else:
            requested_by = user.title
    if stream_type == "Audio":
        stream_media = MediaStream(
            media_path=stream_file,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
            ytdlp_parameters="--cookies cookies.txt",
        )
    elif stream_type == "Video":
        stream_media = MediaStream(
            media_path=stream_file,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
            ytdlp_parameters="--cookies cookies.txt",
        )
    call_status = await get_call_status(chat_id)
    try:
        if call_status == "PLAYING" or call_status == "PAUSED":
            try:
                thumbnail = await create_thumbnail(result_x, user.id)
                position = await add_to_queue(
                    chat_id, user, title, duration, stream_file, stream_type, thumbnail
                )
                caption = f"""ᴀᴅᴅᴇᴅ ᴛᴏ Qᴜᴇᴜᴇ ᴀᴛ : `#{position}`
                
💫 Tɪᴛʟᴇ ❤️  {title}
🗡️ Dᴜʀᴀᴛɪᴏɴ ⏰  {duration}
🔉 Sᴛʀᴇᴀᴍ Tʏᴘᴇ 🔊  {stream_type}
💌 Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ 💌  {requested_by}"""
                await Pbxbot.send_photo(chat_id, thumbnail, caption)
                await stream_logger(
                    chat_id, user, title, duration, stream_type, thumbnail, position
                )
            except Exception as e:
                try:
                    return await aux.edit(f"Qᴜᴇᴜᴇ ᴇʀʀᴏʀ: `{e}`")
                except Exception:
                    LOGGER.info(f"Qᴜᴇᴜᴇ ᴇʀʀᴏʀ: {e}")
                    return
        elif call_status == "IDLE" or call_status == "NOTHING":
            try:
                await call.play(chat_id, stream_media, config=call_config)
            except NoActiveGroupCall:
                try:
                    return await aux.edit_text(f"⚠️ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴄ❗...")
                except Exception:
                    LOGGER.info(f"⚠️ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴄ ({chat_id})❗... ")
                    return
            try:
                thumbnail = await create_thumbnail(result_x, user.id)
                position = await add_to_queue(
                    chat_id, user, title, duration, stream_file, stream_type, thumbnail
                )
                caption = f"""ꜱᴛᴀʀᴛᴇᴅ ꜱᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠᴄ.
                
💫 Tɪᴛʟᴇ ❤️  {title}
🗡️ Dᴜʀᴀᴛɪᴏɴ ⏰  {duration}
🔉 Sᴛʀᴇᴀᴍ Tʏᴘᴇ 🔊  {stream_type}
💌 Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ 💌  {requested_by}"""
                await Pbxbot.send_photo(chat_id, thumbnail, caption)
                await stream_logger(
                    chat_id, user, title, duration, stream_type, thumbnail
                )
            except Exception as e:
                try:
                    return await aux.edit(f"ꜱᴇɴᴅ ᴇʀʀᴏʀ: `{e}`")
                except Exception:
                    LOGGER.info(f"ꜱᴇɴᴅ ᴇʀʀᴏʀ: {e}")
                    return
        else:
            return
        try:
            await aux.delete()
        except Exception:
            pass
        await add_active_media_chat(chat_id, stream_type)
        return
    except Exception as e:
        try:
            return await aux.edit_text(f"ꜱᴛʀᴇᴀᴍ ᴇʀʀᴏʀ: `{e}`")
        except Exception:
            LOGGER.info(f"🚫 ꜱᴛʀᴇᴀᴍ ᴇʀʀᴏʀ: {e}")
            return
  
