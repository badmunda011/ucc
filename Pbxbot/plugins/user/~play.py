import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from pyrogram.types import Message
from . import *
import pygame
pygame.mixer.init()

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait until the music is finished
        pygame.time.Clock().tick(10)

# YTDL options for downloading audio
YTDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",  # Saving file to the correct path
    "noplaylist": True,
    "quiet": True,
    "cookiefile": None,  # Set to None if you don't need cookies
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
        # Search and download the song
        with YoutubeDL(YTDL_OPTS) as ytdl:
            info = ytdl.extract_info(f"ytsearch:{query}", download=True)
            video = info["entries"][0]
            title = video["title"]
            file_path = ytdl.prepare_filename(video).replace(".webm", ".mp3")

        # Check if file exists
        if not os.path.exists(file_path):
            await message.reply("❌ File not found after download. Something went wrong.")
            return

        # Inform the user and play the audio
        await message.reply(f"🎶 Downloaded: **{title}**\nPlaying now...")
        os.system(f"ffplay -nodisp -autoexit '{file_path}'")

        # Cleanup downloaded file
        os.remove(file_path)
        await message.reply("✅ Finished playing!")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")
        
