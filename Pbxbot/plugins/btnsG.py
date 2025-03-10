# G: Glass Buttons

from math import ceil

from pyrogram.types import InlineKeyboardButton, InlineQueryResultPhoto, InlineKeyboardMarkup

from Pbxbot.core import ENV, Symbols, db, Config

from pyrogram import Client, filters
from Pbxbot.core.clients import Pbxbot
bot = Pbxbot.bot


def gen_inline_keyboard(collection: list, row: int = 2) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        kyb = []
        for x in collection[i : i + row]:
            button = btn(*x)
            kyb.append(button)
        keyboard.append(kyb)
    return keyboard


def btn(text, value, type="callback_data") -> InlineKeyboardButton:
    return InlineKeyboardButton(text, **{type: value})


async def gen_inline_help_buttons(page: int, plugins: list) -> tuple[list, int]:
    buttons = []
    column = await db.get_env(ENV.btn_in_help) or 5
    column = int(column)
    emoji = await db.get_env(ENV.help_emoji) or "✧"
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    max_pages = ceil(len(pairs) / column)
    pairs = [pairs[i : i + column] for i in range(0, len(pairs), column)]

    for pair in pairs[page]:
        btn_pair = []
        for i, plugin in enumerate(pair):
            if i % 2 == 0:
                btn_pair.append(
                    InlineKeyboardButton(f"{emoji} {plugin}", f"help_menu:{page}:{plugin}")
                )
            else:
                btn_pair.append(
                    InlineKeyboardButton(f"{plugin} {emoji}", f"help_menu:{page}:{plugin}")
                )
        buttons.append(btn_pair)

    buttons.append(
        [
            InlineKeyboardButton(
                Symbols.previous, f"help_page:{(max_pages - 1) if page == 0 else (page - 1)}",
            ),
            InlineKeyboardButton(
                Symbols.close, "help_data:c"
            ),
            InlineKeyboardButton(
                Symbols.next, f"help_page:{0 if page == (max_pages - 1) else (page + 1)}",
            ),
        ]
    )

    return buttons, max_pages


async def gen_bot_help_buttons() -> list[list[InlineKeyboardButton]]:
    buttons = []
    plugins = sorted(Config.BOT_CMD_MENU)
    emoji = await db.get_env(ENV.help_emoji) or "✧"
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    for pair in pairs:
        btn_pair = []
        for i, plugin in enumerate(pair):
            if i % 2 == 0:
                btn_pair.append(
                    InlineKeyboardButton(f"{emoji} {plugin}", f"bot_help_menu:{plugin}")
                )
            else:
                btn_pair.append(
                    InlineKeyboardButton(f"{plugin} {emoji}", f"bot_help_menu:{plugin}")
                )
        buttons.append(btn_pair)

    buttons.append(
        [
            InlineKeyboardButton("📱", "help_data:start"),
            InlineKeyboardButton(Symbols.close, "help_data:botclose"),
        ]
    )

    return buttons


def start_button() -> list[list[InlineKeyboardButton]]:
    return [
        [
            InlineKeyboardButton("📝 ʜᴇʟᴘ 📝", "help_data:bothelp"),
            InlineKeyboardButton("🗡️ sᴏᴜʀᴄᴇ 🗡️", "help_data:source"),
            ],
        [
            InlineKeyboardButton("📌 DEPLOY 📌", url="https://t.me/PBX_NETWORK/6"),
        ],
        [
        InlineKeyboardButton("🕊️⃝‌ᴘʙx ❤️ᥫ᭡፝֟፝֟" ,  url="https://t.me/ll_THE_BAD_BOT_ll"),
    ]
    ]

@bot.on_inline_query(filters.regex("help_menu"))
async def inline_help(client: Client, inline_query):
    buttons, _ = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU.keys()))
    results = [
        InlineQueryResultPhoto(
            id="help_menu",
            photo_url="https://files.catbox.moe/cv88iq.jpg",
            thumb_url="https://files.catbox.moe/cv88iq.jpg",
            title="Help Menu",
            description="Click to view the help menu",
            caption="📌 **Help Menu:**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    ]
    await inline_query.answer(results, cache_time=0)
