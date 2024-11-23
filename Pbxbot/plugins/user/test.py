import os
import aiofiles
import aiohttp
import aiohtt
import pickle
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


COOKIES_FILE = "cookies.txt"

async def save_cookies(session):
    cookies = session.cookie_jar.filter_cookies()
    async with aiofiles.open(COOKIES_FILE, 'wb') as file:
        await file.write(pickle.dumps(cookies))

async def load_cookies(session):
    if os.path.exists(COOKIES_FILE):
        async with aiofiles.open(COOKIES_FILE, 'rb') as file:
            try:
                cookies = pickle.loads(await file.read())
                session.cookie_jar.update_cookies(cookies)
            except pickle.UnpicklingError:
                print("Invalid cookie file format. Starting fresh...")
                # Reinitialize the cookies file by ignoring its content
                async with aiofiles.open(COOKIES_FILE, 'wb') as reset_file:
                    await reset_file.write(b"")  # Empty file

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
