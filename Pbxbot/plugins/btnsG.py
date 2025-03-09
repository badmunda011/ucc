from math import ceil
from pyrogram.types import InlineKeyboardButton, InlineQueryResultPhoto, InlineKeyboardMarkup
from Pbxbot.core import ENV, Symbols, db, Config

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

async def gen_inline_help_buttons(page: int, plugins: list) -> tuple[list[InlineQueryResultPhoto], int]:
    buttons = []
    photo_url = "https://files.catbox.moe/xduruw.jpg"  # Replace with your photo URL
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
            btn_pair.append(
                InlineKeyboardButton(f"{emoji} {plugin}", f"help_menu:{page}:{plugin}")
                if i % 2 == 0 else 
                InlineKeyboardButton(f"{plugin} {emoji}", f"help_menu:{page}:{plugin}")
            )
        buttons.append(btn_pair)

    buttons.append(
        [
            InlineKeyboardButton(Symbols.previous, f"help_page:{(max_pages - 1) if page == 0 else (page - 1)}"),
            InlineKeyboardButton(Symbols.close, "help_data:c"),
            InlineKeyboardButton(Symbols.next, f"help_page:{0 if page == (max_pages - 1) else (page + 1)}"),
        ]
    )

    # ✅ FIX: Wrap `InlineQueryResultPhoto` in a list
    results = [
        InlineQueryResultPhoto(
            photo_url=photo_url,
            thumb_url=photo_url,
            caption="Help Menu",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    ]

    return results, max_pages  # ✅ Tuple return correctly

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
            btn_pair.append(
                InlineKeyboardButton(f"{emoji} {plugin}", f"bot_help_menu:{plugin}")
                if i % 2 == 0 else 
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
            InlineKeyboardButton("🕊️⃝‌ᴘʙx ❤️ᥫ᭡፝֟፝֟", url="https://t.me/ll_THE_BAD_BOT_ll"),
        ]
    ]
