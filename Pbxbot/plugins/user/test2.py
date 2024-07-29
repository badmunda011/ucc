import os
import random
from asyncio.queues import QueueEmpty
from time import time
import string
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream import *
from pytgcalls import StreamType
from Pbxbot.bad.streamtype import *
from Pbxbot.bad.ults import CHAT_TITLE, gen_thumb
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from pytgcalls import idle as pyidle
from . import *
from Pbxbot.core.config import call_py, contact_filter
from Pbxbot.core.config import *
import re
import asyncio
from pyrogram import Client
from Pbxbot.bad.queues import QUEUE, add_to_queue
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from ntgcalls import TelegramServerError
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import AudioQuality, MediaStream, Update, VideoQuality
from pytgcalls.types.stream import StreamAudioEnded
from youtubesearchpython import VideosSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import yt_dlp
import os

# music player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


# video player
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@on_message("play", allow_stan=True)
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("**🔄 Processing**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/d6f92c979ad96b2031cba.png",
                    caption=f"""
**#⃣ Song Added  {pos}
🏷️ Title: [{songname}]({link})
💬 Chat ID: {chat_id}
🎧 Requested by: {m.from_user.mention}**
""",
                )
            else:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/6213d2673486beca02967.png",
                    caption=f"""
**▶ Start Playing Songs
🏷️ Title: [{songname}]({link})
💬 Chat ID: {chat_id}
🎧 Requested by: {m.from_user.mention}**
""",
                )

    else:
        if len(m.command) < 2:
            await m.reply("Reply to Audio File or provide something for Searching ...")
        else:
            await m.delete()
            huehue = await m.reply("🔎 Searching...")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit("`Didn't Find Anything for the Given Query`")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                srrf = m.chat.title
                ctitle = await CHAT_TITLE(srrf)
                thumb = await gen_thumb(thumbnail, title, userid, ctitle)
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        # await m.reply_to_message.delete()
                        await m.reply_photo(
                            photo=f"{thumb}",
                            caption=f"""
**#⃣ Song Added  {pos}
🏷️ Title: [{songname}]({url})
⏱️ Duration: {duration}
💬 Chat ID: {chat_id}
🎧 Requested by: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{thumb}",
                                caption=f"""
**▶ Start Playing Songs
🏷️ Title: [{songname}]({url})
⏱️ Duration: {duration}
💬 Chat ID: {chat_id}
🎧 Requested by: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@on_message("stram", allow_stan=True)
async def stream(client, m: Message):
   if len(m.command) < 2:
      await m.reply("`Give A Link/LiveLink/.m3u8 URL/YTLink to Play Audio from 🎶`")
   else: 
      link = m.text.split(None, 1)[1]
      huehue = await m.reply("`Trying to Play 📻`")

      # Filtering out YouTube URL's
      regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
      match = re.match(regex,link)
      if match:
         hm, livelink = await ytdl(link)
      else:
         livelink = link
         hm = 1
      
      if hm==0:
         await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
      else:
         if chat_id in QUEUE:
            pos = add_to_queue(chat_id, "Radio 📻", livelink, link, "Audio", 0)
            await huehue.edit(f"Queued at **#{pos}**")
         else:
            try:
               await call_py.join_group_call(
                  chat_id,
                  AudioPiped(
                     livelink,
                  ),
                  stream_type=StreamType().pulse_stream,
               )
               add_to_queue(chat_id, "Radio 📻", livelink, link, "Audio", 0)
               await huehue.edit(f"Started Playing **[Radio 📻]({link})** in `{chat_id}`", disable_web_page_preview=True)
            except Exception as ep:
               await huehue.edit(f"`{ep}`")

