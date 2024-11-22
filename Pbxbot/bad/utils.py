import asyncio
import os
import yt_dlp
from typing import Dict, Union
from asyncio import Queue, QueueEmpty as Empty



class DurationLimitError(Exception):
    pass

class FFmpegReturnCodeError(Exception):
    pass



DURATION_LIMIT = 300



active = []

async def get_active_chats() -> list:
    return active






# ===================================================================================== #


queues: Dict[int, Queue] = {}

async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()

def get(chat_id: int) -> Dict[str, str]:
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except Empty:
            return None

def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True

def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except ValueError:
            pass

def clear(chat_id: int):
    if chat_id in queues:
        if queues[chat_id].empty():
            raise Empty
        else:
            queues[chat_id].queue = []
    raise Empty


# ===================================================================================== #

async def get_audio_stream(link):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    audio = os.path.join(
        "downloads", f"{info['id']}.{info['ext']}"
    )
    if os.path.exists(audio):
        return audio
    x.download([link])
    return audio


async def get_video_stream(link):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    video = os.path.join(
        "downloads", f"{info['id']}.{info['ext']}"
    )
    if os.path.exists(video):
        return video
    x.download([link])
    return video


