import os, aiofiles, aiohttp, ffmpeg, random, re
import requests
from pytgcalls import PyTgCalls as pytgcalls
from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from Pbxbot.bad.utils import get_audio_stream, get_video_stream

# Load cookies from a file (you can customize this path)
COOKIES_PATH = "cookies.txt"

# Utility to read cookies
def load_cookies(filepath):
    cookies = {}
    try:
        with open(filepath, "r") as file:
            for line in file:
                if not line.startswith("#") and line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) >= 7:
                        domain, flag, path, secure, expiry, name, value = parts
                        cookies[name] = value
    except FileNotFoundError:
        print(f"Cookies file not found: {filepath}")
    return cookies

# Load cookies for use
cookies = load_cookies(COOKIES_PATH)

# Updated get_audio_stream and get_video_stream
async def get_audio_stream_with_cookies(url):
    """Fetch audio stream URL using cookies."""
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise Exception(f"Failed to fetch audio stream. Status: {response.status}")

async def get_video_stream_with_cookies(url):
    """Fetch video stream URL using cookies."""
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise Exception(f"Failed to fetch video stream. Status: {response.status}")

# Replace `get_audio_stream` and `get_video_stream` with the new functions
get_audio_stream = get_audio_stream_with_cookies
get_video_stream = get_video_stream_with_cookies

# Integration with YoutubeSearch
async def search_youtube_with_cookies(query):
    """Search YouTube using cookies."""
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.youtube.com/results?search_query={query}"
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.get(search_url) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise Exception(f"Failed to search YouTube. Status: {response.status}")

# Example usage in your `play` function
async def play(_, message):
    query = message.text.split(None, 1)[1]
    try:
        # Search YouTube using cookies
        search_results = await search_youtube_with_cookies(query)
        # Parse results and fetch the first video link (Implement parsing logic)
        # Example: results = YoutubeSearch(search_results, max_results=1).to_dict()
    except Exception as e:
        await message.reply(f"Error while searching YouTube: {e}")
