import os, aiofiles, aiohttp, ffmpeg, random, re
import requests
from Pbxbot.bad.admin_func import authorized_users, admins as a, set_admins as set
from pytgcalls import PyTgCalls as pytgcalls
from typing import Callable
from . import *
from pyrogram import filters, Client
from pyrogram.types import *
from Pbxbot.core import Pbxbot
from youtube_search import YoutubeSearch
from asyncio.queues import QueueEmpty
from pyrogram.errors import UserAlreadyParticipant
from Pbxbot.bad import utils as rq
from Pbxbot.bad.utils import DurationLimitError
from Pbxbot.bad.utils import get_audio_stream, get_video_stream
from pytgcalls.types import Update
from pytgcalls.types import AudioPiped, AudioVideoPiped, AudioQuality, AudioParameters
from Pbxbot.bad.thumb_func import transcode, convert_seconds, time_to_seconds, generate_cover




DURATION_LIMIT = 300

keyboard = InlineKeyboardMarkup([
        [
                InlineKeyboardButton(" •┈┈┈•..........⬬⭒💘⭒⬬.........•┈┈┈• ", url=f"https://t.me/PBX2USERBOT?startgroup=true")
        ],
        [InlineKeyboardButton(" ◁ ", url=f"https://t.me/ll_BAD_ABOUT_ll"),
         InlineKeyboardButton(" ❚❚ ", url=f"https://t.me/ll_THE_BAD_BOT_ll"),
         InlineKeyboardButton(" ▷ ", url=f"https://t.me/ll_BAD_MUNDA_WORLD_ll")
        ],
        [
            InlineKeyboardButton(" ᴄʟᴏsᴇ ", callback_data="close_data"),
        ]
])

local_thumb = [
"https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg",
"https://graph.org/file/5938774f48c1f019c73f7.jpg",
"https://graph.org/file/b13a16734bab174f58482.jpg",
"https://graph.org/file/2deb4e5cbba862f2d5457.jpg",
]


# --------------------------------------------------------------------------------------------------------- #

que = {}
chat_id = None
useer = "NaN"

# --------------------------------------------------------------------------------------------------------- #

@on_message("play", allow_stan=True)
async def play(_, message):
    global que
    global useer    
    chat_id = message.chat.id  
    user_name = message.from_user.mention                
    msg = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**") 
    try:
        user = await Client.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:      
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
        except Exception:    
            await msg.edit_text("**» ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғɪʀsᴛ.**")
        try:
            await Client.join_chat(invitelink)
            await Client.send_message(message.chat.id, text="** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:            
            pass
        except Exception as e:
            await msg.edit_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [🍹𝆺𝅥⃝🌸 ‌⃪‌ ᷟ🦋ᴹᵁˢᴵᶜ ᥫ᭡𓆩ᴾᴸᴬᵞᴱᴿ𓆪🦋☕︎](https://t.me/II_BAD_MUNDA_II)** ")
                            
    audio = ((message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None)
   
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )

        file_path = await message.reply_to_message.download()
        title = audio.file_name 
        link = "https://t.me/ShizuRank_Bot"
        thumbnail = random.choice(local_thumb)
        duration = round(audio.duration / 60)
        views = "Locally added"
        await generate_cover(user_name, title, views, duration, thumbnail)
       
            
    
    else:
        if len(message.command) < 2:
            await msg.edit_text("💌 **ᴜsᴀɢᴇ: /ᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        else:
            await msg.edit_text("**🎧 𝐒ƚαяᴛҽԃ 𝐏ℓαყιɳɠ вαႦყ...**")
                
        query = message.text.split(None, 1)[1]
            
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            
            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60


        except Exception:
            await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ sᴏɴɢ ɴᴀᴍᴇ.**")
            return

        if (dur / 60) > DURATION_LIMIT:
            await msg.edit(f"**sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")
            return

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_audio_stream(link)
            
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{user_name}",
            reply_markup=keyboard,
        )
       
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(
                file_path,
                AudioParameters.from_quality(AudioQuality.STUDIO),
            ),
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}\n",
           )

    os.remove("final.png")
    return await msg.delete()



# --------------------------------------------------------------------------------------------------------- #


@on_message("vplay", allow_stan=True)
async def vplay(_, message):
    global que
    global useer    
    chat_id = message.chat.id  
    user_name = message.from_user.mention                
    msg = await message.reply("**🔎 sᴇᴀʀᴄʜɪɴɢ...**") 
    try:
        user = await Client.get_me()
        await _.get_chat_member(chat_id, user.id)
    except:      
        try:
            invitelink = await _.export_chat_invite_link(chat_id)
        except Exception:    
            await msg.edit_text("**» ᴀᴅᴅ ᴍᴇ ᴀs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ғɪʀsᴛ.**")
        try:
            await Client.join_chat(invitelink)
            await Client.send_message(message.chat.id, text="** ✅ ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ғᴏʀ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        except UserAlreadyParticipant:            
            pass
        except Exception as e:
            await msg.edit_text(f"**ᴘʟᴇᴀsᴇ ᴍᴀɴᴜᴀʟʟʏ ᴀᴅᴅ ᴀssɪsᴛᴀɴᴛ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ [🍹𝆺𝅥⃝🌸 ‌⃪‌ ᷟ🦋ᴹᵁˢᴵᶜ ᥫ᭡𓆩ᴾᴸᴬᵞᴱᴿ𓆪🦋☕︎](https://t.me/II_BAD_MUNDA_II)** ")
                            
    video = (message.reply_to_message.video if message.reply_to_message else None)
   
    if video:
        if round(video.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"** sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**"
            )

        file_path = await message.reply_to_message.download()
        title = video.file_name 
        link = "https://t.me/ShizuRank_Bot"
        thumbnail = random.choice(local_thumb)
        duration = round(video.duration / 60)
        views = "Locally added"
        await generate_cover(user_name, title, views, duration, thumbnail)
       
            
    
    else:
        if len(message.command) < 2:
            await msg.edit_text("💌 **ᴜsᴀɢᴇ: /vᴘʟᴀʏ ɢɪᴠᴇ ᴀ ᴛɪᴛʟᴇ sᴏɴɢ ᴛᴏ ᴘʟᴀʏ ᴍᴜsɪᴄ.**")
        else:
            await msg.edit_text("**🎧 𝐒ƚαяᴛҽԃ 𝐏ℓαყιɳɠ вαႦყ...**")
                
        query = message.text.split(None, 1)[1]
            
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            
            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60


        except Exception:
            await msg.edit("**sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ sᴏɴɢ ɴᴀᴍᴇ.**")
            return

        if (dur / 60) > DURATION_LIMIT:
            await msg.edit(f"**sᴏɴɢs ʟᴏɴɢᴇʀ ᴛʜᴀɴ {DURATION_LIMIT} ᴍɪɴᴜᴛᴇs ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ.**")
            return

        await generate_cover(user_name, title, views, duration, thumbnail)
        file_path = await get_video_stream(link)
            
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await rq.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ ᴛʀᴀᴄᴋ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ » {position} **\n\n**🏷️ ɴᴀᴍᴇ :**[{title[:15]}]({link})\n⏰** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` **ᴍɪɴᴜᴛᴇs**\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏᴇ : **{user_name}",
            reply_markup=keyboard,
        )
       
    else:
        await pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(file_path)
                 
        )
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ sᴛᴀʀᴇᴅ sᴛʀᴇᴀᴍɪɴɢ**\n**🏷️ ɴᴀᴍᴇ : **[{title[:15]}]({link})\n⏰ ** ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}` ᴍɪɴᴜᴛᴇs\n👀 ** ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : **{user_name}\n",
           )

    os.remove("final.png")
    return await msg.delete()






# --------------------------------------------------------------------------------------------------------- #
