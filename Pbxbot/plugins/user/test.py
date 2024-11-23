import os
import aiofiles
import aiohttp
import ffmpeg
import random
import re
import requests
from pyrogram import Client, filters
from pyrogram.types import *
from Pbxbot.core import Pbxbot
from . import *
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioQuality, AudioParameters
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty
import pickle  # Use pickle for serialization/deserialization
import yt_dlp  # Import yt_dlp

async def get_audio_stream(link):
    """Download audio from a YouTube link and return the file path."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",  # Save in "downloads" directory
        "noplaylist": True,
        "quiet": True,
        "cookiefile": "cookies.txt",  # Use cookies to bypass CAPTCHA
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        },
    }

    os.makedirs("downloads", exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        file_path = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

    return file_path

COOKIES_FILE = "cookies.txt"

async def save_cookies(session):
    cookies = session.cookie_jar.filter_cookies()
    async with aiofiles.open(COOKIES_FILE, 'wb') as file:
        await file.write(pickle.dumps(cookies))

async def load_cookies(session):
    if os.path.exists(COOKIES_FILE):
        async with aiofiles.open(COOKIES_FILE, 'rb') as file:
            content = await file.read()
            if not content:  # Check if the file is empty
                print("Cookies file is empty. Skipping loading.")
                return  # Do nothing if the file is empty
            try:
                cookies = pickle.loads(content)
                session.cookie_jar.update_cookies(cookies)
            except (pickle.UnpicklingError, EOFError):
                print("Invalid or empty cookies file. Skipping loading.")
                return

@on_message("play", allow_stan=True)
async def play(client, message):
    if len(message.text.split(None, 1)) < 2:  # Check if there is text after the command
        await message.reply("❌ Please provide a query to search for a song.")
        return

    query = message.text.split(None, 1)[1]  # Safely get the query
    async with aiohttp.ClientSession() as session:
        # Load cookies for session
        await load_cookies(session)

        msg = await message.reply("🔎 Searching...")
        results = YoutubeSearch(query, max_results=1).to_dict()

        if not results:  # Handle case where no results are found
            await msg.edit("❌ No results found for your query.")
            return

        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        duration = results[0]["duration"]

        # Save cookies for future use
        await save_cookies(session)

        # Process song and stream
        file_path = await get_audio_stream(link)  # Define get_audio_stream function
        await pytgcalls.join_group_call(
            message.chat.id,
            AudioPiped(
                file_path,
                AudioParameters.from_quality(AudioQuality.HIGH)
            ),
        )
        await message.reply(f"🎧 Playing: {title}\nDuration: {duration}")
