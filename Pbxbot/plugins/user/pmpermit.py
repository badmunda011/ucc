import random

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from Pbxbot.core import ENV
from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, on_message, bot
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)

blocked_messages = [
    "🤐 User has entered the silent zone.",
    "👻 Message blocked. Ghost mode activated.",
    "🏖️ Sorry, the user is on vacation in Blockland.",
    "🚫 Message blocked. Time for a digital forcefield.",
    "🚷 User temporarily ejected from my DM.",
    "🌑 Blocking vibes only. Silence in progress.",
    "🔇 Shhh... message blocked for tranquility.",
    "🚷 Access denied. User in the digital timeout corner.",
    "⛔ User temporarily MIA from the conversation.",
    "🔒 Message blocked. Secret mission engaged.",
]
unblocked_messages = [
    "🎉 Welcome back! Digital barrier lifted.",
    "🌊 Unblocked! Get ready for a flood of messages.",
    "🗝️ User released from message jail. Freedom at last!",
    "🔓 Breaking the silence!.",
    "📬 User back on the radar. Messages unlocked!",
    "🚀 Soaring back into the conversation!",
    "🌐 Reconnecting user to the chat matrix.",
    "📈 Unblocking for an influx of communication!",
    "🚀 Launching user back into the message cosmos!",
    "🎙️ Unblocked and ready for the conversation spotlight!",
]
WARNS = {}
PREV_MESSAGE = {}


@on_message("block", allow_stan=True)
async def block_user(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user = message.chat
    elif message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "`I can't block myself`")

    if user.id in Config.DEVS:
        return await Pbxbot.delete(message, "`I can't block my devs`")

    success = await client.block_user(user.id)
    if success:
        await Pbxbot.delete(
            message,
            f"**{random.choice(blocked_messages)}\n\n{Symbols.cross_mark} Blocked:** {user.mention}",
        )
    else:
        await Pbxbot.error(message, f"`Couldn't block {user.mention}`")


@on_message("unblock", allow_stan=True)
async def unblock_user(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "`I can't unblock myself`")

    success = await client.unblock_user(user.id)
    if success:
        await Pbxbot.delete(
            message,
            f"**{random.choice(unblocked_messages)}\n\n{Symbols.check_mark} Unblocked:** {user.mention}",
        )
    else:
        await Pbxbot.error(message, f"`Couldn't unblock {user.mention}`")


@on_message(["allow", "approve"], allow_stan=True)
async def allow_pm(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
            user_mention = user.mention
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
        user_mention = message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user_id == client.me.id:
        return await Pbxbot.delete(message, "`I can't allow myself`")

    if await db.is_pmpermit(client.me.id, user_id):
        return await Pbxbot.delete(message, "`User is already allowed to pm!`")

    await db.add_pmpermit(client.me.id, user_id)
    await Pbxbot.delete(message, f"**{Symbols.check_mark} Allowed:** {user_mention}")


@on_message(["disallow", "disapprove"], allow_stan=True)
async def disallow_pm(client: Client, message: Message):
    if len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
            user_id = user.id
            user_mention = user.mention
        except Exception as e:
            return await Pbxbot.error(message, f"`{e}`")
    elif message.chat.type == ChatType.PRIVATE:
        user_id = message.chat.id
        user_mention = message.chat.first_name or message.chat.title
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    else:
        return await Pbxbot.delete(
            message, "`Reply to a user or give their id/username`"
        )

    if user_id == client.me.id:
        return await Pbxbot.delete(message, "`I can't disallow myself`")

    if not await db.is_pmpermit(client.me.id, user_id):
        return await Pbxbot.delete(message, "`User is not allowed to pm!`")

    await db.rm_pmpermit(client.me.id, user_id)
    await Pbxbot.delete(
        message, f"**{Symbols.cross_mark} Disallowed:** {user_mention}"
    )


@on_message(["allowlist", "approvelist"], allow_stan=True)
async def allowlist(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "`Fetching allowlist...`")
    users = await db.get_all_pmpermits(client.me.id)
    if not users:
        return await Pbx.edit("`No users allowed to pm!`")

    text = "**🍀 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽 𝖴𝗌𝖾𝗋'𝗌 𝖫𝗂𝗌𝗍:**\n\n"
    for user in users:
        try:
            name = (await client.get_users(user["user"])).first_name
            text += f"    {Symbols.anchor} {name} (`{user['user']}`) | {user['date']}\n"
        except:
            text += f"    {Symbols.anchor} Unkown Peer (`{user['user']}`) | {user['date']}\n"
            
    await Pbx.edit(text)


@custom_handler(filters.incoming & filters.private & ~filters.bot & ~filters.service)
async def handle_incoming_pm(client: Client, message: Message):
    if message.from_user.id in Config.DEVS:
        return

    if message.from_user.id == 777000:
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
            f"**{Symbols.cross_mark} 𝖤𝗇𝗈𝗎𝗀𝗁 𝗈𝖿 𝗒𝗈𝗎𝗋 𝗌𝗉𝖺𝗆𝗆𝗂𝗇𝗀! 𝖡𝗅𝗈𝖼𝗄𝗂𝗇𝗀 𝗒𝗈𝗎 𝖿𝗋𝗈𝗆 𝖯𝖬.**",
        )

    owner_name = client.me.first_name  # ✅ Owner Ka Name Fetch Kiya
    pm_pic = await db.get_env(ENV.pmpermit_pic) or "https://telegra.ph/file/14166208a7bf871cb0aca.jpg"

    pm_msg = f"👻 **𝐏ʙ𝐗ʙᴏᴛ 2.0 - 𝐏ᴍ 𝐒ᴇᴄᴜʀɪ𝐭ʏ** 👻\n\n"
    pm_msg += f"**👋🏻 𝐇ყ {message.from_user.mention}!**\n❤️ 𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ, 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ 🌪️\n"
    pm_msg += f"⚡ **𝐖αιт 𝐅σя  𝐌у 𝐂υтє [{owner_name}](tg://settings) ❤️**\n\n☠ 𝐘συ 𝐇αʋҽ {warns} 𝐖αɾɳιɳɠʂ 𝐋ҽϝƚ! ☠"

    # ✅ Inline Query Send Karna (Jaisa Ping & Alive Me Hai)
    results = await client.get_inline_bot_results(client.me.username, "pmpermit_menu")
    await client.send_inline_bot_result(message.chat.id, results.query_id, results.results[0].id, True)


@bot.on_inline_query(filters.regex("pmpermit_menu"))
async def inline_pmpermit(client: Client, inline_query):
    pm_pic = await db.get_env(ENV.pmpermit_pic) or "https://telegra.ph/file/14166208a7bf871cb0aca.jpg"

    buttons = [
        [
            InlineKeyboardButton("✅ Allow", callback_data="pm_allow"),
            InlineKeyboardButton("❌ Disallow", callback_data="pm_disallow"),
            InlineKeyboardButton("🚫 Block", callback_data="pm_block"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    results = [
        InlineQueryResultPhoto(
            photo_url=pm_pic,
            thumb_url=pm_pic,
            caption="👻 **𝐏ʙ𝐗ʙᴏᴛ 2.0 - 𝐏ᴍ 𝐒ᴇᴄᴜʀɪ𝐭ʏ** 👻\n\n⚠ **𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐥𝐢𝐦𝐢𝐭𝐞𝐝 𝐚𝐭𝐭𝐞𝐦𝐩𝐭𝐬 𝐭𝐨 𝐬𝐞𝐧𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬!**\n👮‍♂️ **𝐂𝐡𝐨𝐨𝐬𝐞 𝐚𝐧 𝐨𝐩𝐭𝐢𝐨𝐧:**",
            reply_markup=reply_markup,
        )
    ]

    await inline_query.answer(results, cache_time=0)
