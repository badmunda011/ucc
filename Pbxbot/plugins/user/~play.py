import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from pyrogram.types import Message
from . import *

# YTDL options for audio extraction
YTDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",  # Audio file ka name aur extension
    "noplaylist": True,
    "cookiefile": "Pbxbot/cookies.txt",  # Make sure cookies.txt is valid
    "quiet": True,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

# Play music command
@on_message("play", allow_stan=True)
async def play_music(client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("❌ Please provide a song name! Example: `/play Faded`")
        return

    await message.reply(f"🔍 Searching for: **{query}**")

    try:
        # Download the song from YouTube
        with YoutubeDL(YTDL_OPTS) as ytdl:
            info = ytdl.extract_info(f"ytsearch:{query}", download=True)
            title = info["entries"][0]["title"]
            downloaded_file = ytdl.prepare_filename(info["entries"][0])

        # Play the downloaded audio using ffmpeg
        await message.reply(f"🎶 Now playing: **{title}**")
        os.system(f"ffplay -nodisp -autoexit '{downloaded_file}'")

        # Clean up the downloaded file
        os.remove(downloaded_file)
        await message.reply("✅ Finished playing!")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")
        
