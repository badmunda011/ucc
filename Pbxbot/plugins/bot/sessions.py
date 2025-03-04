from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove,
)

from ..btnsG import gen_inline_keyboard, start_button
from ..btnsK import session_keyboard
from . import START_MSG, BotHelp, Config, Symbols, db, Pbxbot


# Existing session menu command
@Pbxbot.bot.on_message(
    filters.command("session") & Config.AUTH_USERS & filters.private
)
async def session_menu(_, message: Message):
    await message.reply_text(
        "**👻 𝖯𝗅𝖾𝖺𝗌𝖾 𝖼𝗁𝗈𝗈𝗌𝖾 𝖺𝗇 𝗈𝗉𝗍𝗂𝗈𝗇 𝖿𝗋𝗈𝗆 𝖻𝖾𝗅𝗈𝗐:**",
        reply_markup=session_keyboard(),
    )


# New command to add session string manually
@Pbxbot.bot.on_message(filters.command("add") & Config.AUTH_USERS & filters.private)
async def add_session(_, message: Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2 or not parts[1]:
        return await message.reply_text("**Error!** Please provide a valid session string.")
    
    session_string = parts[1]
    try:
        client = Client(
            name="Pbxbot 2.0",
            session_string=session_string,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            in_memory=True,
        )
        await client.connect()
        user_id = (await client.get_me()).id
        await db.update_session(user_id, session_string)
        await client.disconnect()
        await message.reply_text(
            "**Success!** Session string added to database."
        )
    except Exception as e:
        await message.reply_text(f"**Error!** {e}")

# Existing command to create a new session
@Pbxbot.bot.on_message(filters.regex(r"ɴᴇᴡ 🔮") & Config.AUTH_USERS & filters.private)
async def new_session(_, message: Message):
    await message.reply_text(
        "**𝖮𝗄𝖺𝗒!** 𝖫𝖾𝗍'𝗌 𝗌𝖾𝗍𝗎𝗉 𝖺 𝗇𝖾𝗐 𝗌𝖾𝗌𝗌𝗂𝗈𝗇",
        reply_markup=ReplyKeyboardRemove(),
    )

    buttons = [
        [
            InlineKeyboardButton(
                " ᴘʙx 2.0 sᴇssɪᴏɴ", 
                web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#pyrogram")
            ),
        ]
    ]

    await message.reply_text(
        "**👻 𝖯𝗅𝖾𝖺𝗌𝖾 𝖼𝗁𝗈𝗈𝗌𝖾 𝖺 𝗇𝖾𝗐 𝗈𝗉𝗍𝗂𝗈𝗇 𝖿𝗋𝗈𝗆 𝖻𝖾𝗅𝗈𝗐:**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# Existing delete session command
@Pbxbot.bot.on_message(
    filters.regex(r"ᴅᴇʟᴇᴛᴇ 🚫") & Config.AUTH_USERS & filters.private
)
async def delete_session(_, message: Message):
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await message.reply_text("𝖭𝗈 𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝗂𝗌𝗍𝗒𝖻𝖺𝗌𝖾.")

    collection = []
    for i in all_sessions:
        collection.append((i["user_id"], f"rm_session:{i['user_id']}"))

    buttons = gen_inline_keyboard(collection, 2)
    buttons.append([InlineKeyboardButton("Cancel ❌", "auth_close")])

    await message.reply_text(
        "**𝖢𝗁𝗈𝗈𝗌𝖾 𝖺 𝗌𝖾𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾:**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# Existing callback query handler to remove session
@Pbxbot.bot.on_callback_query(filters.regex(r"rm_session"))
async def rm_session_cb(client: Client, cb: CallbackQuery):
    collection = []
    user_id = int(cb.data.split(":")[1])
    all_sessions = await db.get_all_sessions()

    if not all_sessions:
        return await cb.message.delete()

    try:
        owner = await client.get_users(Config.OWNER_ID)
        owner_id = owner.id
        owner_name = owner.first_name
    except:
        owner_id = Config.OWNER_ID
        owner_name = "𝖮𝗐𝗇𝖾𝗋"
    if cb.from_user.id not in [user_id, owner_id]:
        return await cb.answer(
            f"𝖠𝖼𝖼𝖾𝗌𝗌 𝗋𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽 𝗍𝗈 𝖺𝗇𝗈𝗍𝗁𝖾𝗋 𝗎𝗌𝖾𝗋𝗌. Only {owner_name} and session client can delete this session.",
            show_alert=True,
        )

    await db.rm_session(user_id)
    await cb.answer("**𝖲𝗎𝖼𝖼𝖾𝗌𝗌!** 𝖲𝖾𝗌𝗌𝗂𝗈𝗇 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗋𝗈𝗆 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾. \n__Restart the bot to apply changes.__")

    for i in all_sessions:
        collection.append((i["user_id"], f"rm_session:{i['user_id']}"))

    buttons = gen_inline_keyboard(collection, 2)
    buttons.append([InlineKeyboardButton("Cancel ❌", "auth_close")])

    await cb.message.edit_reply_markup(InlineKeyboardMarkup(buttons))


# Existing command to list all sessions
@Pbxbot.bot.on_message(filters.regex(r"ʟɪsᴛ 📄") & Config.AUTH_USERS & filters.private)
async def list_sessions(_, message: Message):
    all_sessions = await db.get_all_sessions()
    if not all_sessions:
        return await message.reply_text("𝖭𝗈 𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾.")

    text = f"**{Symbols.cross_mark} 𝖫𝗂𝗌𝗍 𝗈𝖿 𝗌𝖾𝗌𝗌𝗂𝗈𝗇𝗌:**\n\n"
    for i, session in enumerate(all_sessions):
        text += f"[{'0' if i <= 9 else ''}{i+1}] {Symbols.bullet} **𝖴𝗌𝖾𝗋 𝖨𝖣:** `{session['user_id']}`\n"

    await message.reply_text(text)


# Existing command to go home
@Pbxbot.bot.on_message(filters.regex(r"ʜᴏᴍᴇ ⚜️") & filters.private & Config.AUTH_USERS)
async def go_home(_, message: Message):
    await message.reply_text(
        "**Home 🏠**",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.reply_text(
        START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(start_button()),
    )


BotHelp("Sessions").add(
    "session", "This command is packed with tools to manage userbot sessions."
).info(
    "Session 🚀"
).done()
