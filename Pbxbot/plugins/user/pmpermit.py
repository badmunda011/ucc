import random
import time
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto
)

from Pbxbot.core import ENV
from . import Config, db, custom_handler, Pbxbot, bot

WARNS = {}
PREV_MESSAGE = {}

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
            message.chat.id,
            "**🚨 Enough of your spamming! Blocking you.**"
        )

    # Get Bot Owner Info
    bot_info = await client.get_me()
    owner_name = bot_info.first_name
    owner_mention = f"[{owner_name}](tg://user?id={bot_info.id})"

    # Custom PM Message
    pm_msg = "👻 **𝐏ʙ𝐗ʙᴏᴛ 2.0  𝐏ᴍ 𝐒ᴇᴄ𝘂𝗿𝗶𝘁𝘆** 👻\n\n"
    custom_pmmsg = await db.get_env(ENV.custom_pmpermit)

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n\n☠ 𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍! ☠"
    else:
        pm_msg += (
            f"👋🏻 **𝐇ყ {message.from_user.mention}!**\n"
            "❤️ **𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️**\n"
            "⚡ **𝐈ϝ 𝐘συ 𝐒ραɱ , 𝐘συ 𝐖ιℓℓ 𝐁ҽ 𝐁ℓσ¢ƙҽԃ 𝐀υƚσɱαƚι¢ℓℓу 🌸**\n"
            f"🦋 **𝐖αιт 𝐅σя  𝐌у 𝐂υтє {owner_mention} ❤️**\n\n"
            f"☠ **𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!** ☠"
        )

    # Send PM Message
    Pbx = await client.send_message(
        message.chat.id,
        pm_msg,
        disable_web_page_preview=True,
    )

    # Send Inline Buttons
    try:
        result = await client.get_inline_bot_results(bot.me.username, "pmpermit_menu")
        await client.send_inline_bot_result(
            message.chat.id,
            result.query_id,
            result.results[0].id,
            True,
        )
    except Exception as e:
        print(f"Error in PM Permit Inline: {e}")

    PREV_MESSAGE.setdefault(client.me.id, {})[message.from_user.id] = Pbx
    WARNS.setdefault(client.me.id, {})[message.from_user.id] = warns - 1

@bot.on_inline_query(filters.regex("pmpermit_menu"))
async def inline_pmpermit(client: Client, inline_query):
    buttons = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{inline_query.from_user.id}"),
            InlineKeyboardButton("❌ Block", callback_data=f"block_{inline_query.from_user.id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    results = [
        InlineQueryResultPhoto(
            id="pmpermit",
            photo_url="https://files.catbox.moe/y3evsv.jpg",  # Image URL
            thumb_url="https://files.catbox.moe/y3evsv.jpg",  # Thumbnail
            reply_markup=reply_markup  # Removed title, description, and caption
        )
    ]
    
    await inline_query.answer(results, cache_time=0)
