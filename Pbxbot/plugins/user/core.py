import importlib
import os
import sys
from pathlib import Path

from pyrogram import Client
from pyrogram.enums import MessagesFilter, ParseMode
from pyrogram.types import Message

from Pbxbot.core import ENV, Config, Symbols

from . import HelpMenu, bot, db, handler, Pbxbot, on_message


@on_message("help", allow_stan=True)
async def help(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "**Processing...**")
    if len(message.command) == 1:
        try:
            result = await client.get_inline_bot_results(bot.me.username, "help_menu")
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

    plugin = await Pbxbot.input(message)
    if plugin.lower() in Config.CMD_MENU:
        try:
            await Pbxbot.edit(
                Pbx, Config.CMD_MENU[plugin.lower()], ParseMode.MARKDOWN
            )
            return
        except Exception as e:
            await Pbxbot.error(Pbx, str(e), 20)
            return

    available_plugins = f"{Symbols.bullet} **𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗉𝗅𝗎𝗀𝗂𝗇𝗌:**\n\n"
    for i in sorted(list(Config.CMD_MENU.keys())):
        available_plugins += f"`{i}`, "
    available_plugins = available_plugins[:-2]
    available_plugins += (
        f"\n\n𝖣𝗈 `{handler}help <plugin name>` 𝗍𝗈 𝗀𝖾𝗍 𝖽𝖾𝗍𝖺𝗂𝗅𝖾𝖽 𝗂𝗇𝖿𝗈 𝗈𝖿 𝗍𝗁𝖺𝗍 𝗉𝗅𝗎𝗀𝗂𝗇."
    )
    await Pbxbot.edit(Pbx, available_plugins, ParseMode.MARKDOWN)

