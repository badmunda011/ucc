import asyncio
import glob
import importlib
import os
import sys
from pathlib import Path

import pyroaddon  # pylint: disable=unused-import
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import RPCError

from .config import ENV, Config, Symbols
from .database import db
from .logger import LOGS

from pytgcalls import PyTgCalls


class PbxClient(Client):
    def __init__(self) -> None:
        # Initialize `storage` as a dictionary
        self.storage = {}

        self.users: list[Client] = []
        self.bot: Client = Client(
            name="PBXBOT 2.0",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="Pbxbot.plugins.bot"),
        )
        self.call = PyTgCalls(self.bot)  # Ensure this line is correct

    async def is_connected(self) -> bool:
        """Check if the bot is connected"""
        try:
            await self.bot.get_me()
            return True
        except RPCError:
            return False

    async def get_peer_by_id(self, chat_id):
        """Helper to safely retrieve peer by chat ID."""
        try:
            peer = self.call.get_peer_by_id(chat_id)
            return peer
        except AttributeError as e:
            LOGS.error(f"AttributeError in get_peer_by_id: {e}")
            return None
            
            
    async def start_user(self) -> None:
        sessions = await db.get_all_sessions()
        for i, session in enumerate(sessions):
            try:
                client = Client(
                    name=f"PbxUser#{i + 1}",
                    api_id=Config.API_ID,
                    api_hash=Config.API_HASH,
                    session_string=session["session"],
                )
                await client.start()
                me = await client.get_me()
                self.users.append(client)
                LOGS.info(
                    f"{Symbols.arrow_right * 2} Started User {i + 1}: '{me.first_name}' {Symbols.arrow_left * 2}"
                )
                is_in_logger = await self.validate_logger(client)
                if not is_in_logger:
                    LOGS.warning(
                        f"Client #{i+1}: '{me.first_name}' is not in Logger Group! Check and add manually for proper functioning."
                    )
                try:
                    await client.join_chat("https://t.me/ll_THE_BAD_BOT_ll")
                except:
                    pass
                try:
                    await client.join_chat("https://t.me/PBX_NETWORK")
                except:
                    pass
            except Exception as e:
                LOGS.error(f"{i + 1}: {e}")
                continue

    async def start_bot(self) -> None:
        await self.bot.start()
        me = await self.bot.get_me()
        LOGS.info(
            f"{Symbols.arrow_right * 2} Started PbxBot Client: '{me.username}' {Symbols.arrow_left * 2}"
        )

    async def start_pytgcalls(self) -> None:
        try:
            LOGS.info("Starting PyTgCalls...")
            await self.call.start()
            LOGS.info("PyTgCalls Started.")
        except Exception as e:
            LOGS.error(f"Failed To Start PyTgCalls: {e}")

    # Other methods remain unchanged

    async def load_plugin(self) -> None:
        count = 0
        files = glob.glob("Pbxbot/plugins/user/*.py")
        unload = await db.get_env(ENV.unload_plugins) or ""
        unload = unload.split(" ")
        for file in files:
            with open(file) as f:
                path = Path(f.name)
                shortname = path.stem.replace(".py", "")
                if shortname in unload:
                    os.remove(Path(f"Pbxbot/plugins/user/{shortname}.py"))
                    continue
                if shortname.startswith("__"):
                    continue
                fpath = Path(f"Pbxbot/plugins/user/{shortname}.py")
                name = "Pbxbot.plugins.user." + shortname
                spec = importlib.util.spec_from_file_location(name, fpath)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["Pbxbot.plugins.user." + shortname] = load
                count += 1
            f.close()
        LOGS.info(
            f"{Symbols.bullet * 3} Loaded User Plugin: '{count}' {Symbols.bullet * 3}"
        )

    async def load_plugin(self, bot_client: Client = None) -> None:
    """Load plugins for user or bot."""
    count = 0
    folder = "Pbxbot/plugins/bad" if bot_client is None else "Pbxbot/bad"
    files = glob.glob(f"{folder}/*.py")
    unload = await db.get_env(ENV.unload_plugins) or ""
    unload = unload.split(" ")
    for file in files:
        with open(file) as f:
            path = Path(f.name)
            shortname = path.stem.replace(".py", "")
            if shortname in unload:
                os.remove(Path(f"{folder}/{shortname}.py"))
                continue
            if shortname.startswith("__"):
                continue
            fpath = Path(f"{folder}/{shortname}.py")
            name = f"{folder.replace('/', '.')}.{shortname}"
            spec = importlib.util.spec_from_file_location(name, fpath)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[name] = load
            count += 1
        f.close()
    LOGS.info(
        f"{Symbols.bullet * 3} Loaded Plugins: '{count}' from {folder} {Symbols.bullet * 3}"
    )

async def start_all_bots(self) -> None:
    """Start all bots saved in the database."""
    bot_sessions = await db.get_all_bot_sessions()
    for session in bot_sessions:
        try:
            bot_client = Client(
                name=f"PbxBot-{session['bot_id']}",
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                bot_token=session["bot_token"],
                plugins=dict(root="Pbxbot.bad"),  # Load plugins for the bot
            )
            await bot_client.start()
            self.users.append(bot_client)  # Keep track of all running clients
            LOGS.info(f"Started Bot: {session['bot_id']}")
        except Exception as e:
            LOGS.error(f"Failed to start bot {session['bot_id']}: {e}")
            continue
  

    async def validate_logger(self, client: Client) -> bool:
        try:
            await client.get_chat_member(Config.LOGGER_ID, "me")
            return True
        except Exception:
            return await self.join_logger(client)

    async def join_logger(self, client: Client) -> bool:
        try:
            invite_link = await self.bot.export_chat_invite_link(Config.LOGGER_ID)
            await client.join_chat(invite_link)
            return True
        except Exception:
            return False

    async def start_message(self, version: dict) -> None:
        await self.bot.send_animation(
            Config.LOGGER_ID,
            "https://telegra.ph/file/48a4bb97b1b6e64184223.mp4",
            f"**{Symbols.check_mark} ᴘʙx 2.0 ɪs.ɴᴏᴡ ᴏɴʟɪɴᴇ!**\n\n"
            f"**{Symbols.triangle_right}  ᴄʟɪᴇɴᴛs ➠ ** `{len(self.users)}`\n"
            f"**{Symbols.triangle_right} ᴘʟᴜɢɪɴs ➠ ** `{len(Config.CMD_MENU)}`\n"
            f"**{Symbols.triangle_right} ᴄᴏᴍᴍᴀɴᴅs ➠ ** `{len(Config.CMD_INFO)}`\n"
            f"**{Symbols.triangle_right} sᴛᴀɴ ᴜsᴇʀs ➠ ** `{len(Config.STAN_USERS)}`\n"
            f"**{Symbols.triangle_right} ᴀᴜᴛʜ ᴜsᴇʀs ➠ ** `{len(Config.AUTH_USERS)}`\n\n"
            f"**{Symbols.triangle_right} ᴘʙx 2.0 ᴠᴇʀsɪᴏɴ ➠ ** `{version['Pbxbot']}`\n"
            f"**{Symbols.triangle_right}  ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ ➠ ** `{version['pyrogram']}`\n"
            f"**{Symbols.triangle_right}  ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ➠ ** `{version['python']}`\n\n"
            f"**</> @ll_THE_BAD_BOT_ll**",
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💫 sᴛᴀʀᴛ ᴍᴇ",
                            url=f"https://t.me/{self.bot.me.username}?start=start",
                        ),
                        InlineKeyboardButton(
                            "💖 ʀᴇᴘᴏ", url="https://github.com/Badhacker98/PBX_2.0/fork"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "⎯꯭̽🇨🇦꯭꯭ ⃪В꯭α꯭∂ ꯭м꯭υ꯭η∂꯭α_꯭آآ⎯꯭ ꯭̽🌸",
                            url="https://t.me/ll_BAD_MUNDA_ll",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "🦋 𝐏ʙx 𝐁ᴏᴛ 𝐒ᴜᴘᴘᴏʀᴛ ❤️",
                            url="https://t.me/ll_THE_BAD_BOT_ll",
                        ),
                    ],
                ]
            ),
        )

    async def startup(self) -> None:
        LOGS.info(
            f"{Symbols.bullet * 3} Starting PBX 2.0 Client & User {Symbols.bullet * 3}"
        )
        await self.start_bot()
        await self.start_user()
        await self.start_pytgcalls()
        await self.start_all_bots()
        await self.load_plugin()


class CustomMethods(PbxClient):
    # Custom methods can remain unchanged
    pass


Pbxbot = CustomMethods()
call = Pbxbot.call

class CustomMethods(PbxClient):
    async def input(self, message: Message) -> str:
        """Get the input from the user"""
        if len(message.command) < 2:
            output = ""

        else:
            try:
                output = message.text.split(" ", 1)[1].strip() or ""
            except IndexError:
                output = ""
        
        # Correct way to access chat ID
        chat_id = message.chat.id  # Accessing chat.id correctly

        return output

    async def edit(
        self,
        message: Message,
        text: str,
        parse_mode: ParseMode = ParseMode.DEFAULT,
        no_link_preview: bool = True,
    ) -> Message:
        """Edit or Reply to a message, if possible"""
        if message.from_user and message.from_user.id in Config.STAN_USERS:
            if message.reply_to_message:
                return await message.reply_to_message.reply_text(
                    text,
                    parse_mode=parse_mode,
                    disable_web_page_preview=no_link_preview,
                )
            return await message.reply_text(
                text, parse_mode=parse_mode, disable_web_page_preview=no_link_preview
            )
        return await message.edit_text(
            text, parse_mode=parse_mode, disable_web_page_preview=no_link_preview
        )

    async def _delete(self, message: Message, delay: int = 0) -> None:
        """Delete a message after a certain period of time"""
        await asyncio.sleep(delay)
        await message.delete()

    async def delete(
        self, message: Message, text: str, delete: int = 10, in_background: bool = True
    ) -> None:
        """Edit a message and delete it after a certain period of time"""
        to_del = await self.edit(message, text)
        if in_background:
            asyncio.create_task(self._delete(to_del, delete))
        else:
            await self._delete(to_del, delete)

    async def error(self, message: Message, text: str, delete: int = 10) -> None:
        """Edit an error message and delete it after a certain period of time if mentioned"""
        to_del = await self.edit(message, f"{Symbols.cross_mark} **Error:** \n\n{text}")
        if delete:
            asyncio.create_task(self._delete(to_del, delete))

    async def _log(self, tag: str, text: str, file: str = None) -> None:
        """Log a message to the Logger Group"""
        msg = f"**#{tag.upper()}**\n\n{text}"
        try:
            if file:
                try:
                    await self.bot.send_document(Config.LOGGER_ID, file, caption=msg)
                except:
                    await self.bot.send_message(
                        Config.LOGGER_ID, msg, disable_web_page_preview=True
                    )
            else:
                await self.bot.send_message(
                    Config.LOGGER_ID, msg, disable_web_page_preview=True
                )
        except Exception as e:
            raise Exception(f"{Symbols.cross_mark} LogErr: {e}")

    async def check_and_log(self, tag: str, text: str, file: str = None) -> None:
        """Check if :
        \n-> the Logger Group is available
        \n-> the logging is enabled"""
        status = await db.get_env(ENV.is_logger)
        if status and status.lower() == "true":
            await self._log(tag, text, file)



Pbxbot = CustomMethods()

# Expose the call instance for external imports
call = Pbxbot.call

