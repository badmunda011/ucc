import os
import random
import asyncio
from time import time
import string
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
import AudioPiped

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

audio_piped = True

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


# YTDL
# https://github.com/pytgcalls/pytgcalls/blob/dev/example/youtube_dl/youtube_dl_example.py
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


@on_message("play", allow_stan=True)
async def play(client, m: Message):
        replied = m.reply_to_message
        chat_id = m.chat.id
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❤️ ᴏᴡɴᴇʀ ❤️", url=f"https://t.me/Dr_Asad_Ali"
                    ),
                    InlineKeyboardButton(
                        "👨‍‍👧‍👦 ɢʀᴏᴜᴘ 👨‍👧‍👦", url=f"https://t.me/Shayri_Music_Lovers"
                    ),
                ]
            ]
        )
        if replied:
            if replied.audio or replied.voice:
                huehue = await replied.reply("👨‍⚖️ **Aɴᴀʟʏsɪɴɢ...**")
                dl = await replied.download()
                link = replied.link
                if replied.audio:
                    if replied.audio.title:
                        songname = replied.audio.title[:15] + "..."
                    else:
                        if replied.audio.file_name:
                            songname = replied.audio.file_name[:15] + "..."
                        else:
                            songname = "Audio"
                elif replied.voice:
                    songname = "Voice Note"
                if chat_id in QUEUE:
                    pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await huehue.edit(f"Queued at **#{pos}**")
                else:
                    try:
                        await call_py.join_group_call(
                            chat_id,
                            AudioPiped(
                                dl,
                            ),
                            stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                        await huehue.edit(
                            f"🎶 **sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ ▶** \n**🎧 sᴏɴɢ** : [{songname[:15]}] \n**💬 ᴄʜᴀᴛ** : `{chat_id}`"
                        )
                    except Exception as hmme:
                        await huehue.edit(hmme)
            else:
                if len(m.command) < 2:
                    await m.reply(
                        "😜 **ʀᴇᴘʟᴀʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ᴏʀ ɢɪᴠᴇ ᴍᴇ ᴀ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ sᴇᴀʀᴄʜ**"
                    )
                else:
                    huehue = await m.reply("🔎 **Sᴇᴀʀᴄʜɪɴɢ...**")
                    query = m.text.split(None, 1)[1]
                    search = ytsearch(query)
                    if search == 0:
                        await huehue.edit("🤔 **ɴᴏᴛʜɪɴɢ ғᴏᴜɴᴅ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ sᴇᴀʀᴄʜ**")
                    else:
                        songname = search[0]
                        url = search[1]
                        hm, ytlink = await ytdl(url)
                        if hm == 0:
                            await huehue.edit(
                                f"**YTDL ERROR ⚠️** ᴄᴏɴᴛᴀᴄᴛ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](t.me/Dr_Asad_Ali)",
                                disable_web_page_preview=True,
                            )
                        else:
                            if chat_id in QUEUE:
                                pos = add_to_queue(
                                    chat_id, songname, ytlink, url, "Audio", 0
                                )
                                await huehue.edit(
                                    f"**ʏᴏᴜʀ sᴏɴɢ ɪs ᴀᴛ ᴡᴀɪᴛɪɴɢ ᴘᴏsɪᴛɪᴏɴ** 👉 **#{pos}**"
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
                                    add_to_queue(
                                        chat_id, songname, ytlink, url, "Audio", 0
                                    )
                                    await huehue.edit(
                                        f"🎶 **sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ ▶** \n**🎧 sᴏɴɢ** : [{songname[:15]}] \n**💬 ᴄʜᴀᴛ** : `{chat_id}`"
                                    )
                                except Exception as ep:
                                    await huehue.edit(f"`{ep}`")

        else:
            if len(m.command) < 2:
                await m.reply(
                    "😜 **ʀᴇᴘʟᴀʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ᴏʀ ɢɪᴠᴇ ᴍᴇ ᴀ sᴏᴍᴇᴛʜɪɴɢ ᴛᴏ sᴇᴀʀᴄʜ**"
                )
            else:
                huehue = await m.reply("🔎 **Sᴇᴀʀᴄʜɪɴɢ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await huehue.edit("🤔 **ɴᴏᴛʜɪɴɢ ғᴏᴜɴᴅ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ sᴇᴀʀᴄʜ**")
                else:
                    songname = search[0]
                    url = search[1]
                    hm, ytlink = await ytdl(url)
                    if hm == 0:
                        await huehue.edit(
                            f"**YTDL ERROR ⚠️** ᴄᴏɴᴛᴀᴄᴛ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](t.me/Dr_Asad_Ali)",
                            disable_web_page_preview=True,
                        )
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await huehue.edit(
                                f"**ʏᴏᴜʀ sᴏɴɢ ɪs ᴀᴛ ᴡᴀɪᴛɪɴɢ ᴘᴏsɪᴛɪᴏɴ** 👉 **#{pos}**"
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
                                await huehue.edit(
                                    f"🎶 **sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ ▶** \n**🎧 sᴏɴɢ** : [{songname[:15]}] \n**💬 ᴄʜᴀᴛ** : `{chat_id}`"
                                )
                            except Exception as ep:
                                await huehue.edit(f"`{ep}`")


@on_message("stream", allow_stan=True)
async def stream(client, m: Message):
        chat_id = m.chat.id
        if len(m.command) < 2:
            await m.reply(
                "`Give A Link/LiveLink/.m3u8 URL/YTLink to Play Audio from 🎶`"
            )
        else:
            link = m.text.split(None, 1)[1]
            huehue = await m.reply("`Trying to Play 📻`")

            # Filtering out YouTube URL's
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, link)
            if match:
                hm, livelink = await ytdl(link)
            else:
                livelink = link
                hm = 1

            if hm == 0:
                await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
            else:
                if chat_id in QUEUE:
                    pos = add_to_queue(chat_id, "Radio 📻", livelink, link, "Audio", 0)
                    await huehue.edit(
                        f"**ʏᴏᴜʀ sᴏɴɢ ɪs ᴀᴛ ᴡᴀɪᴛɪɴɢ ᴘᴏsɪᴛɪᴏɴ** 👉 **#{pos}**"
                    )
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
                        await huehue.edit(
                            f"Started Playing **[Radio 📻]({link})** in `{chat_id}`",
                            disable_web_page_preview=True,
                        )
                    except Exception as ep:
                        await huehue.edit(f"`{ep}`")
                      

#musicplay


@on_message("playy", allow_stan=True)
async def playfrom(client, m: Message):
        chat_id = m.chat.id
        if len(m.command) < 2:
            await m.reply(
                "**USAGE:** \n\n`/playfrom [chat_id/username]` \n`/playfrom [chat_id/username] ; [no. of songs]`"
            )
        else:
            args = m.text.split(maxsplit=1)[1]
            if ";" in args:
                chat = args.split(";")[0]
                limit = int(args.split(";")[1])
            else:
                chat = args
                limit = 10
            hmm = await m.reply(f"Searching the last **{limit}** Songs from `{chat}`")
            try:
                async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                    location = await x.download()
                    if x.audio.title:
                        songname = x.audio.title[:30] + "..."
                    else:
                        if x.audio.file_name:
                            songname = x.audio.file_name[:30] + "..."
                        else:
                            songname = "Audio"
                    link = x.link
                    if chat_id in QUEUE:
                        add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    else:
                        await call_py.join_group_call(
                            chat_id,
                            AudioPiped(location),
                            stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, location, link, "Audio", 0)
                        await m.reply(
                            f"**Started Playing Songs from {chat} ▶** \n**🎧 SONG** : [{songname}]({link}) \n**💬 CHAT** : `{chat_id}`",
                            disable_web_page_preview=True,
                        )
                await hmm.delete()
                await m.reply(f"Added **{limit}** SONGS to Queue")
            except Exception as e:
                await hmm.edit(f"**ERROR** \n`{e}`")


#vcplay


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:35] + "..."
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


# YTDL
# https://github.com/pytgcalls/pytgcalls/blob/dev/example/youtube_dl/youtube_dl_example.py
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


@on_message("vplay", allow_stan=True)
async def vplay(client, m: Message):
    if GRPPLAY or (m.from_user and m.from_user.is_contact) or m.outgoing:
        replied = m.reply_to_message
        chat_id = m.chat.id
        if replied:
            if replied.video or replied.document:
                huehue = await replied.reply("`Downloading`")
                dl = await replied.download()
                link = replied.link
                if len(m.command) < 2:
                    Q = 720
                else:
                    pq = m.text.split(None, 1)[1]
                    if pq == "720" or "480" or "360":
                        Q = int(pq)
                    else:
                        Q = 720
                        await huehue.edit(
                            "`Only 720, 480, 360 Allowed` \n`Now Streaming in 720p`"
                        )
                try:
                    if replied.video:
                        songname = replied.video.file_name[:35] + "..."
                    elif replied.document:
                        songname = replied.document.file_name[:35] + "..."
                except:
                    songname = "Video"

                if chat_id in QUEUE:
                    pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                    await huehue.edit(f"Queued at **#{pos}**")
                else:
                    if Q == 720:
                        hmmm = HighQualityVideo()
                    elif Q == 480:
                        hmmm = MediumQualityVideo()
                    elif Q == 360:
                        hmmm = LowQualityVideo()
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                        stream_type=StreamType().pulse_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "Video", Q)
                    await huehue.edit(
                        f"**Started Playing Video ▶** \n**🎧 SONG** : [{songname}]\n**💬 CHAT** : `{chat_id}`",
                        disable_web_page_preview=True,
                    )
            else:
                if len(m.command) < 2:
                    await m.reply(
                        "`Reply to an Audio File or give something to Search`"
                    )
                else:
                    huehue = await m.reply("`Searching...`")
                    query = m.text.split(None, 1)[1]
                    search = ytsearch(query)
                    Q = 720
                    hmmm = HighQualityVideo()
                    if search == 0:
                        await huehue.edit("`Found Nothing for the Given Query`")
                    else:
                        songname = search[0]
                        url = search[1]
                        hm, ytlink = await ytdl(url)
                        if hm == 0:
                            await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
                        else:
                            if chat_id in QUEUE:
                                pos = add_to_queue(
                                    chat_id, songname, ytlink, url, "Video", Q
                                )
                                await huehue.edit(f"Queued at **#{pos}**")
                            else:
                                try:
                                    await call_py.join_group_call(
                                        chat_id,
                                        AudioVideoPiped(
                                            ytlink, HighQualityAudio(), hmmm
                                        ),
                                        stream_type=StreamType().pulse_stream,
                                    )
                                    add_to_queue(
                                        chat_id, songname, ytlink, url, "Video", Q
                                    )
                                    await huehue.edit(
                                        f"**Started Playing Video ▶** \n**🎧 SONG** : [{songname}] \n**💬 CHAT** : `{chat_id}`",
                                        disable_web_page_preview=True,
                                    )
                                except Exception as ep:
                                    await huehue.edit(f"`{ep}`")

        else:
            if len(m.command) < 2:
                await m.reply("`Reply to an Audio File or give something to Search`")
            else:
                huehue = await m.reply("`Searching...`")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                hmmm = HighQualityVideo()
                if search == 0:
                    await huehue.edit("`Found Nothing for the Given Query`")
                else:
                    songname = search[0]
                    url = search[1]
                    hm, ytlink = await ytdl(url)
                    if hm == 0:
                        await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await huehue.edit(f"Queued at **#{pos}**")
                        else:
                            try:
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),
                                    stream_type=StreamType().pulse_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await huehue.edit(
                                    f"**Started Playing Video ▶** \n**🎧 SONG** : [{songname}] \n**💬 CHAT** : `{chat_id}`",
                                    disable_web_page_preview=True,
                                )
                            except Exception as ep:
                                await huehue.edit(f"`{ep}`")


@on_message("vsyram", allow_stan=True)
async def vstream(client, m: Message):
        chat_id = m.chat.id
        if len(m.command) < 2:
            await m.reply("`Give A Link/LiveLink/.m3u8 URL/YTLink to Stream from 🎶`")
        else:
            if len(m.command) == 2:
                link = m.text.split(None, 1)[1]
                Q = 720
                huehue = await m.reply("`Trying to Stream 💭`")
            elif len(m.command) == 3:
                op = m.text.split(None, 1)[1]
                link = op.split(None, 1)[0]
                quality = op.split(None, 1)[1]
                if quality == "720" or "480" or "360":
                    Q = int(quality)
                else:
                    Q = 720
                    await m.reply(
                        "`Only 720, 480, 360 Allowed` \n`Now Streaming in 720p`"
                    )
                huehue = await m.reply("`Trying to Stream 💭`")
            else:
                await m.reply("`!vstream {link} {720/480/360}`")

            # Filtering out YouTube URL's
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex, link)
            if match:
                hm, livelink = await ytdl(link)
            else:
                livelink = link
                hm = 1

            if hm == 0:
                await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
            else:
                if chat_id in QUEUE:
                    pos = add_to_queue(
                        chat_id, "Live Stream 📺", livelink, link, "Video", Q
                    )
                    await huehue.edit(f"Queued at **#{pos}**")
                else:
                    if Q == 720:
                        hmmm = HighQualityVideo()
                    elif Q == 480:
                        hmmm = MediumQualityVideo()
                    elif Q == 360:
                        hmmm = LowQualityVideo()
                    try:
                        await call_py.join_group_call(
                            chat_id,
                            AudioVideoPiped(livelink, HighQualityAudio(), hmmm),
                            stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(
                            chat_id, "Live Stream 📺", livelink, link, "Video", Q
                        )
                        await huehue.edit(
                            f"Started **[Live Stream 📺]({link})** in `{chat_id}`",
                            disable_web_page_preview=True,
                        )
                    except Exception as ep:
                        await huehue.edit(f"`{ep}`")
                        
