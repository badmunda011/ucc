import random
import os
import sys
from BadAPI import api
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty
from pyrogram.enums import ChatAction, ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from Pbxbot import db
from Pbxbot.bad import chatai
import asyncio

translator = GoogleTranslator()

lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status


async def get_chat_language(chat_id):
    chat_lang = await lang_db.find_one({"chat_id": chat_id})
    return chat_lang["language"] if chat_lang and "language" in chat_lang else None
   
    
@Client.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    chat_id = message.chat.id
    chat_status = await status_db.find_one({"chat_id": chat_id})
    if chat_status:
        current_status = chat_status.get("status", "not found")
        await message.reply(f"Chatbot status for this chat: **{current_status}**")
    else:
        await message.reply("No status found for this chat.")


@Client.on_message(filters.command(["resetlang", "nolang"]))
async def reset_language(client: Client, message: Message):
    chat_id = message.chat.id
    lang_db.update_one({"chat_id": chat_id}, {"$set": {"language": "nolang"}}, upsert=True)
    await message.reply_text("**Bot language has been reset in this chat to mix language.**")


@Client.on_message(filters.command("chatbot"))
async def chatbot_command(client: Client, message: Message):
    command = message.text.split()
    if len(command) > 1:
        flag = command[1].lower()
        chat_id = message.chat.id
        if flag in ["on", "enable"]:
            status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "enabled"}}, upsert=True)
            await message.reply_text(f"ᴄʜᴀᴛʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ **enabled** for this chat ✅.")
        elif flag in ["off", "disable"]:
            status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True)
            await message.reply_text(f"ᴄʜᴀᴛʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ **disabled** ꜰᴏʀ ᴛʜɪꜱ ᴄʜᴀᴛ ❌.")
        else:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴏᴘᴛɪᴏɴ! ᴜꜱᴇ `/chatbot on` or `/chatbot off`.")
    else:
        await message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪꜱᴀʙʟᴇ ᴛʜᴇ ᴄʜᴀᴛʙᴏᴛ.\n\n"
            "ᴇxᴀᴍᴘʟᴇ: `/chatbot on` or `/chatbot off`"
        )



@Client.on_message(filters.command(["lang", "language", "setlang"]))
async def set_language(client: Client, message: Message):
    command = message.text.split()
    if len(command) > 1:
        lang_code = command[1]
        chat_id = message.chat.id
        lang_db.update_one({"chat_id": chat_id}, {"$set": {"language": lang_code}}, upsert=True)
        await message.reply_text(f"Language has been set to `{lang_code}`.")
    else:
        await message.reply_text(
            "Please provide a language code after the command to set your chat language.\n"
            "**Example:** `/lang en`\n\n"
            "**Language code list with names:**"
            f"{languages}"
        )
