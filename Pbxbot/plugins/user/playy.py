from pytgcalls.types.input_stream import InputStream, AudioPiped
from pyrogram.types import Message
from . import HelpMenu, group_only, on_message, Pbxbot
import asyncio
import os
from yt_dlp import YoutubeDL
from Pbxbot.core.clients import PyTgCalls

vc_player = PyTgCalls(Pbxbot)
vc_queues = {}

ydl_opts = {
    'format': 'bestaudio',
    'quiet': True,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
}

@on_message("play", chat_type=group_only)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Give a song name or link.")

    query = message.text.split(None, 1)[1]
    await message.reply("🔍 Searching...")
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        file_path = ydl.prepare_filename(info)
        if message.chat.id not in vc_queues:
            vc_queues[message.chat.id] = []
        vc_queues[message.chat.id].append(file_path)
        if len(vc_queues[message.chat.id]) > 1:
            return await message.reply("✅ Added to queue.")
        
        await vc_player.join_group_call(
            message.chat.id,
            InputStream(AudioPiped(file_path))
        )
        await message.reply(f"▶️ Playing: `{info['title']}`")

@on_message("pause", chat_type=group_only)
async def pause_cmd(_, m: Message):
    await vc_player.pause_stream(m.chat.id)
    await m.reply("⏸️ Paused.")

@on_message("resume", chat_type=group_only)
async def resume_cmd(_, m: Message):
    await vc_player.resume_stream(m.chat.id)
    await m.reply("▶️ Resumed.")

@on_message("skip", chat_type=group_only)
async def skip_cmd(_, m: Message):
    queue = vc_queues.get(m.chat.id)
    if queue and len(queue) > 1:
        os.remove(queue.pop(0))
        next_song = queue[0]
        await vc_player.change_stream(
            m.chat.id,
            InputStream(AudioPiped(next_song))
        )
        await m.reply("⏭️ Skipped to next song.")
    else:
        await m.reply("❌ Queue empty.")

@on_message("leave", chat_type=group_only)
async def leave_cmd(_, m: Message):
    await vc_player.leave_group_call(m.chat.id)
    vc_queues.pop(m.chat.id, None)
    await m.reply("👋 Left VC.")
