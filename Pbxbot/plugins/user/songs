import os
import asyncio
import requests
import time
import yt_dlp
from youtube_search import YoutubeSearch
from pyrogram import filters
from pyrogram import filters
from pyrogram.types import Message
from time import time
import asyncio
from lyricsgenius import Genius
from pyrogram import Client
from pyrogram.errors import MessageTooLong
from yt_dlp import YoutubeDL

from Pbxbot.core import ENV
from Pbxbot.functions.driver import YoutubeDriver
from Pbxbot.functions.paste import post_to_telegraph
from Pbxbot.functions.tools import progress

from . import HelpMenu, Symbols, db, Pbxbot, on_message

# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 20 commands within 60 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5
# -------------------


# -------------------------------------------------------------------------------


@on_message("song", allow_stan=True)
async def download_song(_, message):
    user_id = message.from_user.id
    current_time = time()
    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    query = " ".join(message.command[1:])
    print(query)
    m = await message.reply("**🔄 sᴇᴀʀᴄʜɪɴɢ... **")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

        # Add these lines to define views and channel_name
        views = results[0]["views"]
        channel_name = results[0]["channel"]

    except Exception as e:
        await m.edit(
            "**⚠️ ɴᴏ ʀᴇsᴜʟᴛs ᴡᴇʀᴇ ғᴏᴜɴᴅ. ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ᴛʏᴘᴇᴅ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ sᴏɴɢ ɴᴀᴍᴇ**"
        )
        print(str(e))
        return
    await m.edit("**💫 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("**✅ ᴜᴘʟᴏᴀᴅɪɴɢ...**")

        await message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"{title}\nRᴇǫᴜᴇsᴛᴇᴅ ʙʏ ➪{message.from_user.mention}\nVɪᴇᴡs➪ {views}\nCʜᴀɴɴᴇʟ➪ {channel_name}",
            duration=dur,
        )
        await m.delete()
    except Exception as e:
        await m.edit(" - An error !!")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


# ------------------------------------------------------------------------------- #

###### INSTAGRAM REELS DOWNLOAD


@on_message("ig", allow_stan=True)
async def download_instareels(_, message: Message):
    user_id = message.from_user.id
    current_time = time()
    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    try:
        reel_ = m.command[1]
    except IndexError:
        await m.reply_text("Give me an link to download it...")
        return
    if not reel_.startswith("https://www.instagram.com/reel/"):
        await m.reply_text(
            "In order to obtain the requested reel, a valid link is necessary. Kindly provide me with the required link."
        )
        return
    OwO = reel_.split(".", 1)
    Reel_ = ".dd".join(OwO)
    try:
        await m.reply_video(Reel_)
        return
    except Exception:
        try:
            await m.reply_photo(Reel_)
            return
        except Exception:
            try:
                await m.reply_document(Reel_)
                return
            except Exception:
                await m.reply_text("I am unable to reach to this reel.")


######


@on_message("reel", allow_stan=True)
async def instagram_reel(_, message: Message):
    user_id = message.from_user.id
    current_time = time()
    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    if len(message.command) == 2:
        url = message.command[1]
        response = requests.post(
            f"https://lexica-api.vercel.app/download/instagram?url={url}"
        )
        data = response.json()

        if data["code"] == 2:
            media_urls = data["content"]["mediaUrls"]
            if media_urls:
                video_url = media_urls[0]["url"]
                await message.reply_video(f"{video_url}")
            else:
                await message.reply(
                    "No video found in the response. may be accountbis private."
                )
        else:
            await message.reply("Request was not successful.")
    else:
        await message.reply(
            "Please provide a valid Instagram URL using the /reels command."
        )

@on_message("lyrics", allow_stan=True)
async def getlyrics(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to fetch lyrics.")

    api = await db.get_env(ENV.lyrics_api)
    if not api:
        return await Pbxbot.delete(message, "Lyrics API not found.")

    query = await Pbxbot.input(message)
    if "-" in query:
        artist, song = query.split("-")
    else:
        artist, song = "", query

    Pbx = await Pbxbot.edit(message, f"🔎 __𝖫𝗒𝗋𝗂𝖼𝗌 𝖲𝗈𝗇𝗀__ `{query}`...")

    genius = Genius(
        api,
        verbose=False,
        remove_section_headers=True,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
    )

    song = genius.search_song(song, artist)
    if not song:
        return await Pbxbot.delete(Pbx, "No results found.")

    title = song.full_title
    image = song.song_art_image_url
    artist = song.artist
    lyrics = song.lyrics

    outStr = f"<b>{Symbols.anchor} Title:</b> <code>{title}</code>\n<b>{Symbols.anchor} Artist:</b> <code>{artist}</code>\n\n<code>{lyrics}</code>"
    try:
        await Pbx.edit(outStr, disable_web_page_preview=True)
    except MessageTooLong:
        content = f"<img src='{image}'/>\n\n{outStr}"
        url = post_to_telegraph(title, content)
        await Pbx.edit(
            f"**{Symbols.anchor} Title:** `{title}`\n**{Symbols.anchor} Artist:** `{artist}`\n\n**{Symbols.anchor} Lyrics:** [Click Here]({url})",
            disable_web_page_preview=True,
        )


HelpMenu("songs").add(
    "song",
    "<song name>",
    "Download the given audio song from Youtube!",
    "song believer",
).add(
    "video",
    "<song name>",
    "Download the given video song from Youtube!",
    "song believer",
).add(
    "lyrics",
    "<song name>",
    "Get the lyrics of the given song! Give artist name after - to get accurate results.",
    "lyrics believer - imagine dragons",
    "Need to setup Lyrics Api key from https://genius.com/developers",
).info(
    "Song and Lyrics"
).done()
