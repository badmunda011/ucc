import os
import asyncio
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from . import *
from pyrogram.types import Message
from io import BytesIO

# Function to handle the search and music play
async def search_and_play_music(query, message):
    YTDL_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": "%(title)s.%(ext)s",
    "noplaylist": True,
    "cookiefile": "cookies.txt",  # Path to your exported cookies file
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
        # Use yt-dlp to download the audio in the background
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

        # Use asyncio.to_thread for non-blocking audio file reading and sending
        await send_audio(message, file_path, title)

        # Clean up after playing
        os.remove(file_path)
        await message.reply("✅ Finished playing!")

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

# Function to handle sending audio asynchronously
async def send_audio(message, file_path, title):
    loop = asyncio.get_event_loop()
    
    # Run file reading and sending asynchronously
    audio_stream = await loop.run_in_executor(None, read_audio_file, file_path)

    # Send the audio to the chat
    await message.reply_audio(audio_stream, caption=f"Now playing: **{title}**")

# Helper function to read audio file and return as a byte stream
def read_audio_file(file_path):
    with open(file_path, "rb") as audio_file:
        return BytesIO(audio_file.read())

# Handle incoming messages for searching and playing music
@Client.on_message(filters.command("play") & filters.private)
async def play_music(client, message):
    query = " ".join(message.command[1:])  # Get the query from the message
    if not query:
        await message.reply("❌ Please provide a song name.")
        return
    await search_and_play_music(query, message)
