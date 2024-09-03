from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from . import *
from . import Pbxbot
#--------------------------

MUST_JOIN = "PBX_CHAT"
MUST_JOIN2 = "HEROKUBIN_01"
MUST_JOIN3 = "ll_THE_BAD_BOT_ll"
MUST_JOIN4 = "ll_BAD_MUNDA_WORLD_ll"

#------------------------
@Pbxbot.bot.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN,MUST_JOIN2,MUST_JOIN3,MUST_JOIN4, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
                link2 = "https://t.me/" + MUST_JOIN2
                link3 = "https://t.me/" + MUST_JOIN3
                link4 = "https://t.me/" + MUST_JOIN4
                
            else:
                chat_info = await app.get_chat(MUST_JOIN,MUST_JOIN2,MUST_JOIN3,MUST_JOIN4)
                link = chat_info.invite_link
                link2 = chat_info.invite_link
                link3 = chat_info.invite_link
                link4 = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://telegra.ph/file/afdb310aefd322f49de79.jpg", caption=f"๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ , ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ ᴊᴏɪɴ  ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ ! ",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("๏Jᴏɪɴº๏", url=link),
                            ],
                            [
                            InlineKeyboardButton("๏Jᴏɪɴ¹๏", url=link2),
                            ],
                            [
                            InlineKeyboardButton("๏Jᴏɪɴ²๏", url=link3),
                            ],
                            [
                            InlineKeyboardButton("๏Jᴏɪɴ³๏", url=link4),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"๏ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴍᴜsᴛ_Jᴏɪɴ ᴄʜᴀᴛ ๏: {MUST_JOIN} !")
