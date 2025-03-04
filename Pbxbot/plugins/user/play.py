import os
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL
from dotenv import load_dotenv
from youtubesearchpython import VideosSearch
from . import HelpMenu, group_only, handler, Pbxbot, on_message, Config
from Pbxbot.core.clients import PyTgCalls  # Custom PyTgCalls import
from pyrogram import Client
from pytgcalls import PyTgCalls

# Assuming Pbxbot is an instance of PbxClient initialized elsewhere
call = Pbxbot.call


# Load environment variables
load_dotenv()

COOKIE_PATH = "cookies.txt"  # Cookies ka file path

async def get_thumb(videoid):
    try:
        query = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(query, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail
    except Exception:
        return "https://i.imgur.com/0vYOHlL.jpg"  # Default Thumbnail

def get_audio_url(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "cookiefile": COOKIE_PATH,  # Cookies file use karega authentication ke liye
        "extract_audio": True,
        "audio_format": "mp3",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if "entries" in info:
            return info["entries"][0]["url"], info["entries"][0]["id"]
        return None, None

@on_message(
    "play",
    "vplay",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def play_music(_, message):
    if len(message.command) < 2:
        return await message.reply("Usage: /play song_name")

    query = " ".join(message.command[1:])
    url, videoid = get_audio_url(query)

    if not url:
        return await message.reply("Song not found!")

    thumb = await get_thumb(videoid)
    
    chat_id = message.chat.id
    await call.join_group_call(chat_id, AudioPiped(url))  # Pbxbot ka PyTgCalls use ho raha hai
    await message.reply_photo(thumb, caption=f"🎵 Playing: {query}")

@on_message(
    "stop",
    "end",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def stop_music(_, message):
    chat_id = message.chat.id
    await call.leave_group_call(chat_id)
    await message.reply("⏹ Music Stopped!")
