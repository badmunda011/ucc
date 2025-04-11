from pyrogram import Client, filters
from pyrogram.types import Message
import time

@client.on_message(filters.command("ping") & filters.private)
    async def ping_command(_, message: Message):
        start_time = time.time()  # Current time in seconds
        reply = await message.reply_text("🏓 Pong!")
        end_time = time.time()  # Time after reply is sent
        ping_time = round((end_time - start_time) * 1000)  # Calculate ping in ms
        await reply.edit_text(f"🏓 Pong! `{ping_time}ms`")
