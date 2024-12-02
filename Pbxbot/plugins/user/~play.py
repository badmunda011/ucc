import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from pyrogram.types import Message
import subprocess
from . import *

# Function to handle the search and music play
async def search_and_play_music(query, message):
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
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    }
    try:
        with YoutubeDL(YTDL_OPTS) as ytdl:
            info = ytdl.extract_info(f"ytsearch:{query}", download=True)
            video = info["entries"][0]
            title = video["title"]
            file_path = ytdl.prepare_filename(video).replace(".webm", ".mp3")

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found at {file_path}")  # Debugging line
            await message.reply(f"❌ The file {title} could not be found after download.")
            return

        # Inform user about the successful download
        await message.reply(f"🎶 Downloaded: **{title}**\nPlaying now...")

        # Play the downloaded audio using ffmpeg
        subprocess.run(["ffmpeg", "-i", file_path, "-f", "mp3", "-acodec", "mp3", "pipe:1"])

        # Clean up after playing
        os.remove(file_path)
        await message.reply("✅ Finished playing!")

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

# Handle incoming messages for searching and playing music
@on_message("play", allow_stan=True)
async def play_music(client, message):
    query = " ".join(message.command[1:])  # Get the query from the message
    if not query:
        await message.reply("❌ Please provide a song name.")
        return
    await search_and_play_music(query, message)
