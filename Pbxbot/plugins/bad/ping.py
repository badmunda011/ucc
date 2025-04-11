from pyrogram import Client, filters
from pyrogram.types import Message
import time


@client.on_message(filters.command("ping") & filters.private)
async def ping_command(client, message: Message):
    start_time = time.time()  # Record the current time
    reply = await message.reply_text("🏓 Pong!")  # Send initial reply
    end_time = time.time()  # Record the time after reply
    ping_time = round((end_time - start_time) * 1000)  # Calculate ping in milliseconds
    await reply.edit_text(f"🏓 Pong! `{ping_time}ms`")  # Edit reply with ping time

# Run the bot
