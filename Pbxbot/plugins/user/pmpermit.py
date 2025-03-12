import random
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery
)

from Pbxbot.core import ENV
from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, on_message, bot

WARNS = {}
PREV_MESSAGE = {}

# ✅ PM Permit Handler with Proper Buttons
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
            f"**{Symbols.cross_mark} Enough of your spamming! Blocking you.**"
        )

    pm_msg = f"👻 𝐏ʙ𝐗ʙᴏᴛ 2.0  𝐏ᴍ 𝐒ᴇᴄᴜʀɪᴛʏ 👻\n\n"
    custom_pmmsg = await db.get_env(ENV.custom_pmpermit)

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n**You have {warns} warnings left!**"
    else:
        pm_msg += f"**👋🏻 Hey {message.from_user.mention}!**\n❤️ My Owner is offline, please don't spam. \n⚡ If you spam, you will be blocked!"

    # ✅ Buttons with Callback Data
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.from_user.id}")],
            [InlineKeyboardButton("❌ Block", callback_data=f"block_{message.from_user.id}")]
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
                reply_markup=buttons,  # ✅ Ensure this is properly added
            )
    except Exception as e:
        print(f"Error in PM Permit: {e}")
        msg = await client.send_message(
            message.chat.id,
            pm_msg,
            disable_web_page_preview=True,
            reply_markup=buttons,  # ✅ Ensure this is properly added
        )

    # ✅ Store previous message to delete if needed
    prev_msg = PREV_MESSAGE.get(client.me.id, {}).get(message.from_user.id, None)
    if prev_msg:
        await prev_msg.delete()

    PREV_MESSAGE.setdefault(client.me.id, {})[message.from_user.id] = msg
    WARNS.setdefault(client.me.id, {})[message.from_user.id] = warns - 1

# ✅ Callback Query Handler for PM Permit
@bot.on_callback_query(filters.regex(r"approve_(\d+)"))
async def approve_user(client: Client, query: CallbackQuery):
    user_id = int(query.matches[0].group(1))
    await db.approve_pmpermit(client.me.id, user_id)
    await query.message.edit_text("✅ User Approved!")

@bot.on_callback_query(filters.regex(r"block_(\d+)"))
async def block_user(client: Client, query: CallbackQuery):
    user_id = int(query.matches[0].group(1))
    await client.block_user(user_id)
    await query.message.edit_text("❌ User Blocked!")
