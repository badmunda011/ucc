import importlib
import os
import sys
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.enums import MessagesFilter, ParseMode
from pyrogram.types import InlineQueryResultPhoto
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent

from Pbxbot.core import ENV, Config, Symbols

from . import HelpMenu, bot, db, handler, Pbxbot, on_message

@on_message("repo", allow_stan=True)
async def repo(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "**Repo...**")
    try:
        result = await client.get_inline_bot_results(bot.me.username, "repo_menu")
        await client.send_inline_bot_result(
            message.chat.id,
            result.query_id,
            result.results[0].id,
            True,
        )
        return await Pbx.delete()
    except Exception as e:
        await Pbxbot.error(Pbx, str(e), 20)
        return
        
@bot.on_inline_query(filters.regex("repo_menu"))
async def inline_repo(client: Client, inline_query):
    buttons = [
        [
            InlineKeyboardButton("ʀᴇᴘᴏ", url="https://github.com/Badhacker98/PBX_2.0/fork")
        ],
        [
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/HEROKUBIN_01"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/PBX_CHAT")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    results = [
        InlineQueryResultPhoto(
            id="repo",
            photo_url="https://files.catbox.moe/y3evsv.jpg",  # Image URL
            thumb_url="https://files.catbox.moe/y3evsv.jpg",  # Thumbnail
            title="Repository Information",
            description="Click to view the repository details",
            caption="📌 **Repo:**\n🔗 [Click Here](https://github.com/Badhacker98/PBX_2.0/fork)",
            reply_markup=reply_markup
        )
    ]
    
    await inline_query.answer(results, cache_time=0)

