import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    InlineQueryResultArticle, 
    InputTextMessageContent
)

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

# ✅ Function to Get PM Permit Buttons with Callback Data
def get_pmpermit_buttons():
    return [
        [
            InlineKeyboardButton("✅ Approve", callback_data="approve_user"),
            InlineKeyboardButton("❌ Block", callback_data="block_user"),
        ]
    ]

# ✅ PM Permit Handler
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
            f"**{Symbols.cross_mark} 𝖤𝗇𝗈𝗎𝗀𝗁 𝗈𝖿 𝗒𝗈𝗎𝗋 𝗌𝗉𝖺𝗆𝗆𝗂𝗇𝗀! 𝖡𝗅𝗈𝖼𝗄𝗂𝗇𝗀 𝗒𝗈𝗎.**"
        )

    pm_msg = f"👻 𝐏ʙ𝐗ʙᴏᴛ 2.0  𝐏ᴍ 𝐒ᴇᴄᴜʀɪᴛʏ 👻\n\n"
    custom_pmmsg = await db.get_env(ENV.custom_pmpermit)

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n**𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!**"
    else:
        pm_msg += f"**👋🏻 𝐇ყ {message.from_user.mention}!**\n❤️ 𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ, 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️ \n⚡ 𝐈ϝ 𝐘συ 𝐒ρα�[...]"

    buttons = get_pmpermit_buttons()  # Callback buttons use kar rahe hain
    reply_markup = InlineKeyboardMarkup(buttons)

    try:
        pm_pic = await db.get_env(ENV.pmpermit_pic)
        if pm_pic:
            msg = await client.send_photo(
                message.from_user.id,
                photo=pm_pic,
                caption=pm_msg,
                reply_markup=reply_markup,
            )
        else:
            msg = await client.send_message(
                message.from_user.id,
                pm_msg,
                disable_web_page_preview=True,
                reply_markup=reply_markup,
            )
    except:
        msg = await client.send_message(
            message.from_user.id,
            pm_msg,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
        )

    prev_msg = PREV_MESSAGE.get(client.me.id, {}).get(message.from_user.id, None)
    if prev_msg:
        await prev_msg.delete()

    PREV_MESSAGE[client.me.id] = {message.from_user.id: msg}
    WARNS[client.me.id] = {message.from_user.id: warns - 1}

# ✅ Callback Query Handler for PM Permit
@bot.on_callback_query(filters.regex("approve_user"))
async def approve_user(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    await db.approve_pmpermit(client.me.id, user_id)
    await query.message.edit_text("✅ User Approved!")

@bot.on_callback_query(filters.regex("block_user"))
async def block_user(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    await client.block_user(user_id)
    await query.message.edit_text("❌ User Blocked!")
