import random
import time
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Pbxbot.core import ENV
from . import Config, db, custom_handler, Pbxbot, bot

WARNS = {}
PREV_MESSAGE = {}

# ✅ PM Permit Handler (With Fixed Buttons)
@custom_handler(filters.incoming & filters.private & ~filters.bot & ~filters.service)
async def handle_incoming_pm(client: Client, message: Message):
    if message.from_user.id in Config.DEVS or message.from_user.id == 777000:
        return

    if await db.is_pmpermit(client.me.id, message.from_user.id):
        return

    if message.from_user.id in Config.AUTH_USERS:
        return

    max_spam = await db.get_env(ENV.pm_max_spam)
    max_spam = int(max_spam) if max_spam else 3
    warns = WARNS.get(client.me.id, {}).get(message.from_user.id, max_spam)

    if warns <= 0:
        await client.block_user(message.from_user.id)
        WARNS[client.me.id] = {message.from_user.id: max_spam}
        return await client.send_message(
            message.from_user.id,
            "**🚨 Enough of your spamming! Blocking you.**"
        )

    pm_msg = (
        "👻 **𝐏ʙ𝐗ʙᴏᴛ 2.0  𝐏ᴍ 𝐒ᴇᴄᴜʀɪᴛʏ** 👻\n\n"
        f"👋🏻 **Hey {message.from_user.mention}!**\n"
        "❤️ **My Owner is offline, please don't spam.**\n"
        "⚡ **If you spam, you will be blocked!**\n\n"
        "🔹 **Choose an option below:**"
    )

    bot_username = client.me.username  # Bot username fetch

    # ✅ Fixed Buttons (Using URL Instead of Callback)
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Approve", url=f"https://t.me/{bot_username}?start=approve_{message.from_user.id}")],
            [InlineKeyboardButton("❌ Block", url=f"https://t.me/{bot_username}?start=block_{message.from_user.id}")],
        ]
    )

    try:
        pm_pic = await db.get_env(ENV.pmpermit_pic)
        if pm_pic:
            msg = await client.send_photo(
                message.chat.id,
                photo=pm_pic,
                caption=pm_msg,
                reply_markup=buttons,
            )
        else:
            msg = await client.send_message(
                message.chat.id,
                pm_msg,
                disable_web_page_preview=True,
                reply_markup=buttons,
            )
    except Exception as e:
        print(f"Error in PM Permit: {e}")
        msg = await client.send_message(
            message.chat.id,
            pm_msg,
            disable_web_page_preview=True,
            reply_markup=buttons,
        )

    prev_msg = PREV_MESSAGE.get(client.me.id, {}).get(message.from_user.id, None)
    if prev_msg:
        await prev_msg.delete()

    PREV_MESSAGE.setdefault(client.me.id, {})[message.from_user.id] = msg
    WARNS.setdefault(client.me.id, {})[message.from_user.id] = warns - 1
