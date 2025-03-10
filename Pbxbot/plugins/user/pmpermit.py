import random

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from Pbxbot.core import ENV
from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, on_message, bot

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
            f"**{Symbols.cross_mark} 𝖤𝗇𝗈𝗎𝗀𝗁 𝗈𝖿 𝗒𝗈𝗎𝗋 𝗌𝗉𝖺𝗆𝗆𝗂𝗇𝗀 𝗁𝖾𝗋𝖾! 𝖡𝗅𝗈𝖼𝗄𝗂𝗇𝗀 𝗒𝗈𝗎 𝖿𝗋𝗈𝗆 𝖿𝗎𝗋𝗍𝗁𝖾𝗋 𝖼𝗈𝗇𝗍𝖺𝖼𝗍𝖾𝗍𝗂𝗏𝗂𝗍𝗒!**"
        )

    pm_msg = f"👻 𝐏ʙ𝐗ʙᴏᴛ 2.0  𝐏ᴍ 𝐒ᴇᴄᴜʀɪᴛʏ 👻\n\n"
    custom_pmmsg = await db.get_env(ENV.custom_pmpermit)

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n**𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!**"
    else:
        pm_msg += f"**👋🏻𝐇ყ {message.from_user.mention}!**\n❤️𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️ \n⚡𝐈ϝ 𝐘συ 𝐒ραɱ, 𝐘συ 𝐖ιℓℓ 𝐁ε 𝐁ℓσ𝐜κεԃ!**"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Allow", callback_data=f"allow_pm_{message.from_user.id}"),
                InlineKeyboardButton("🚫 Disallow", callback_data=f"disallow_pm_{message.from_user.id}")
            ],
            [
                InlineKeyboardButton("🔒 Block", callback_data=f"block_{message.from_user.id}"),
                InlineKeyboardButton("🔓 Unblock", callback_data=f"unblock_{message.from_user.id}")
            ]
        ]
    )

    try:
        pm_pic = await db.get_env(ENV.pmpermit_pic)
        if pm_pic:
            msg = await client.send_document(
                message.from_user.id,
                pm_pic,
                caption=pm_msg,
                reply_markup=buttons,
                force_document=False,
            )
        else:
            msg = await client.send_message(
                message.from_user.id,
                pm_msg,
                reply_markup=buttons,
                disable_web_page_preview=True,
            )
    except:
        msg = await client.send_message(
            message.from_user.id,
            pm_msg,
            reply_markup=buttons,
            disable_web_page_preview=True,
        )

    prev_msg = PREV_MESSAGE.get(client.me.id, {}).get(message.from_user.id, None)
    if prev_msg:
        await prev_msg.delete()

    PREV_MESSAGE[client.me.id] = {message.from_user.id: msg}
    WARNS[client.me.id] = {message.from_user.id: warns - 1}


@bot.on_callback_query(filters.regex(r"^(allow_pm|disallow_pm|block|unblock)_(\d+)$"))
async def pmpermit_callback(client, query):
    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "allow_pm":
        if await db.is_pmpermit(client.me.id, user_id):
            return await query.answer("User is already allowed!", show_alert=True)
        await db.add_pmpermit(client.me.id, user_id)
        await query.answer("User allowed to PM!")
        await query.message.edit_text(f"✅ {user_id} is now allowed to PM!")

    elif action == "disallow_pm":
        if not await db.is_pmpermit(client.me.id, user_id):
            return await query.answer("User is not allowed!", show_alert=True)
        await db.rm_pmpermit(client.me.id, user_id)
        await query.answer("User disallowed from PM!")
        await query.message.edit_text(f"🚫 {user_id} is now disallowed from PM!")

    elif action == "block":
        await client.block_user(user_id)
        await query.answer("User blocked!")
        await query.message.edit_text(f"🔒 {user_id} has been blocked!")

    elif action == "unblock":
        await client.unblock_user(user_id)
        await query.answer("User unblocked!")
        await query.message.edit_text(f"🔓 {user_id} has been unblocked!")


@bot.on_inline_query(filters.regex("pmpermit"))
async def inline_pmpermit(client, inline_query):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Allow", callback_data="allow_pm"),
                InlineKeyboardButton("🚫 Disallow", callback_data="disallow_pm")
            ],
            [
                InlineKeyboardButton("🔒 Block", callback_data="block"),
                InlineKeyboardButton("🔓 Unblock", callback_data="unblock")
            ]
        ]
    )

    result = [
        InlineQueryResultArticle(
            title="PM Permit Settings",
            description="Manage PM permissions using inline mode.",
            input_message_content=InputTextMessageContent("👻 PM Permit Settings"),
            reply_markup=buttons,
        )
    ]
    await inline_query.answer(result, cache_time=0)
