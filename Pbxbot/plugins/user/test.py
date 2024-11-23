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
from pytgcalls.types import AudioPiped, AudioVideoPiped, AudioQuality, AudioParameters
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty


# Initialize cookies file path
COOKIES_FILE = "cookies.txt"

# Function to save cookies
async def save_cookies(session):
    async with aiofiles.open(COOKIES_FILE, 'wb') as file:
        cookies = session.cookie_jar.filter_cookies()
        await file.write(cookies.serialize())

# Function to load cookies
async def load_cookies(session):
    if os.path.exists(COOKIES_FILE):
        async with aiofiles.open(COOKIES_FILE, 'rb') as file:
            cookies = await file.read()
            session.cookie_jar.update_cookies(cookies)


# Example usage: Play command
@on_message("play", allow_stan=True)
async def play(client, message):
    async with aiohttp.ClientSession() as session:
        # Load cookies for session
        await load_cookies(session)

        msg = await message.reply("🔎 Searching...")
        query = message.text.split(None, 1)[1]
        results = YoutubeSearch(query, max_results=1).to_dict()

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
        
