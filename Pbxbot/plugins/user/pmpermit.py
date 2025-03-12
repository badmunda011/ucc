import random
import time
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from Pbxbot.core import ENV
from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, bot

WARNS = {}
PREV_MESSAGE = {}

# ✅ Inline Query for PM Permit Buttons
@bot.on_inline_query(filters.regex("pmpermit_menu"))
async def inline_pmpermit(client: Client, inline_query):
    bot_username = client.me.username  # Bot username dynamically fetch karenge

    buttons = [
        [
            InlineKeyboardButton("✅ Approve", callback_data="approve"),
            InlineKeyboardButton("❌ Block", callback_data="block"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    results = [
        InlineQueryResultArticle(
            id="pmpermit",
            title="PM Permit Options",
            description="Block or Approve users",
            input_message_content=InputTextMessageContent("Select an action for PM Permit:"),
            reply_markup=reply_markup
        )
    ]

    await inline_query.answer(results, cache_time=0)


# ✅ PM Permit Handler Using Inline Buttons
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

    bot_username = client.me.username

    # ✅ Use Inline Query to Generate Buttons
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⚙️ PM Permit Options", switch_inline_query_current_chat="pmpermit_menu")]
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
