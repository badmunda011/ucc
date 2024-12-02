import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from pyrogram.types import Message
from . import *
import pygame
import os
import re

def shorten_filename(filename, max_length=255):
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename

file_path = os.path.join("downloads", shorten_filename(video["title"]) + ".mp3")

# Ensure the downloads directory exists
os.makedirs("downloads", exist_ok=True)

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait until the music is finished
        pygame.time.Clock().tick(10)

# YTDL options for downloading audio
YTDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",  # Ensuring correct output path
    "noplaylist": True,
    "quiet": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "cookiefile": "Pbxbot/cookies.txt",  # Optional, remove if not needed
}

# Ensure downloads directory exists
os.makedirs("downloads", exist_ok=True)

# Play command
@on_message("play", allow_stan=True)
async def play_music(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("❌ Please provide a song name! Example: `/play Faded`")
        return

    await message.reply(f"🔍 Searching for: **{query}**")

    try:
        with YoutubeDL(YTDL_OPTS) as ytdl:
        info = ytdl.extract_info(f"ytsearch:{query}", download=True)
        video = info["entries"][0]
        title = video["title"]
        file_path = ytdl.prepare_filename(video).replace(".webm", ".mp3")

    # Check if the file exists after download
    if not os.path.exists(file_path):
        print(f"File not found at {file_path}")  # Debugging line
        await message.reply(f"❌ The file {title} could not be found after download.")
        return

    # Inform user about the successful download
    await message.reply(f"🎶 Downloaded: **{title}**\nPlaying now...")
    
    # Play the downloaded audio (you can use ffmpeg or pygame here)
    os.system(f"ffplay -nodisp -autoexit '{file_path}'")

    # Cleanup the downloaded file after playing
    os.remove(file_path)
    await message.reply("✅ Finished playing!")

except Exception as e:
    await message.reply(f"❌ Error: {str(e)}")
