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
from . import Config, HelpMenu, Symbols, custom_handler, db, Pbxbot, on_message

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
        pm_msg += f"{custom_pmmsg}\n\n☠ 𝐘𝗈𝗎 𝐇𝖺𝗏𝖾 {warns} 𝐖𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝐋𝖾𝖿𝗍! ☠"
    else:
        pm_msg += (
            f"👋🏻 **𝐇ყ {message.from_user.mention}!**\n"
            "❤️ **𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️**\n"
            "⚡ **𝐈ϝ 𝐘συ 𝐒ραɱ , 𝐘συ 𝐖ιℓℓ 𝐁ҽ 𝐁ℓσ¢ƙҽԃ 𝐀υƚσɱαƚι¢ℓℓу 🌸**\n"
            f"🦋 **𝐖αιт 𝐅σя  𝐌у 𝐂υтє {owner_mention} ❤️**\n\n"
            f"☠ **𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝐖𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝐋𝖾𝖿𝗍!** ☠"
        )

    try:
        result = await client.get_inline_bot_results(bot.me.username, f"pmpermit_menu_{message.from_user.id}")
        await client.send_inline_bot_result(
            message.chat.id,
            result.query_id,
            result.results[0].id,
            True,
        )
    except Exception as e:
        print(f"Error in PM Permit Inline: {e}")

    WARNS.setdefault(client.me.id, {})[message.from_user.id] = warns - 1

@bot.on_inline_query(filters.regex(r"pmpermit_menu_(\d+)"))
async def inline_pmpermit(client: Client, inline_query):
    user_id = int(inline_query.matches[0].group(1))

    # Get Bot Owner Info
    bot_info = await client.get_me()
    owner_name = bot_info.first_name
    owner_mention = f"[{owner_name}](tg://user?id={bot_info.id})"
    

    # Custom PM Message
    pm_msg = "👻 **𝐏ʙ𝐗ʙᴏᴛ 2.0  𝐏ᴍ 𝐒ᴇᴄ𝘂𝗿𝗶𝘁𝘆** 👻\n\n"
    custom_pmmsg = await db.get_env(ENV.custom_pmpermit)

    warns = WARNS.get(client.me.id, {}).get(user_id, 3)

    if custom_pmmsg:
        pm_msg += f"{custom_pmmsg}\n\n☠ 𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍! ☠"
    else:
        pm_msg += (
            f"👋🏻 **𝐇ყ 𝐈m {inline_query.from_user.mention}!**\n"
            "❤️ **𝐎ɯɳҽɾ 𝐈ʂ 𝐎ϝϝℓιɳҽ 𝐒ꪮ 𝐏ℓꫀαʂꫀ 𝐃σɳ'ƚ 𝐒ραɱ🌪️**\n"
            "⚡ **𝐈ϝ 𝐘συ 𝐒ραɱ , 𝐘συ 𝐖ιℓℓ 𝐁ҽ 𝐁ℓσ¢ƙҽԃ 𝐀υƚσɱαƚι¢ℓℓу 🌸**\n"
            f"🦋 **𝐖αιт 𝐅σя  𝐌у 𝐂υтє {inline_query.from_user.mention} ❤️**\n\n"
            f"☠ **𝐘𝗈𝗎 𝗁𝖺𝗏𝖾 {warns} 𝗐𝖺𝗋𝗇𝗂𝗇𝗀𝗌 𝗅𝖾𝖿𝗍!** ☠"
        )

    buttons = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
            InlineKeyboardButton("❌ Block", callback_data=f"block_{user_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Inline Query Result with Photo + Text + Button in One Message
    results = [
        InlineQueryResultPhoto(
            id=f"pmpermit_{user_id}",
            photo_url="https://files.catbox.moe/f7eemn.jpg",  # Image URL
            thumb_url="https://files.catbox.moe/f7eemn.jpg",  # Thumbnail
            caption=pm_msg,  # Fixed Error: Now Caption is Defined
            reply_markup=reply_markup  # Buttons Below Image + Text
        )
    ]
    
    await inline_query.answer(results, cache_time=0)
    
    
    
HelpMenu("pmpermit").add(
    "block",
    "<reply to user>/<userid/username>",
    "Block a user from pm-ing you.",
    "block @ll_THE_BAD_BOT_ll",
).add(
    "unblock",
    "<reply to user>/<userid/username>",
    "Unblock a user from pm-ing you.",
    "unblock @ll_THE_BAD_BOT_ll",
).add(
    "allow",
    "<reply to user>/<userid/username>",
    "Allow a user to pm you.",
    "allow @ll_THE_BAD_BOT_ll",
    "An alias of 'approve' is also available.",
).add(
    "disallow",
    "<reply to user>/<userid/username>",
    "Disallow a user to pm you.",
    "disallow @ll_THE_BAD_BOT_ll",
    "An alias of 'disapprove' is also available.",
).add(
    "allowlist",
    None,
    "List all users allowed to pm you.",
    "allowlist",
    "An alias of 'approvelist' is also available.",
).info(
    "Manage who can pm you."
).done()
