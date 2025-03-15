import os 
import io
import shutil 
import random, re
import glob
import time
import requests
import random
from PIL import Image, ImageDraw, ImageFont
from MukeshRobot.modules.nightmode import button_row
from MukeshRobot import BOT_USERNAME, OWNER_ID,BOT_NAME, SUPPORT_CHAT, telethn
from MukeshRobot.events import register
from MukeshRobot import telethn as tbot
from telethon.tl.types import InputMessagesFilterPhotos
from io import BytesIO
from requests import get
from . import Config, HelpMenu, db, Pbxbot, on_message

LOGO_LINKS = [
    "https://telegra.ph/file/d1838efdafce9fe611d0c.jpg",
    "https://telegra.ph/file/c1ff2d5ec5e1b5bd1b200.jpg",
    "https://telegra.ph/file/08c5fbe14cc4b13d1de05.jpg",
    "https://telegra.ph/file/66614a049d74fe2a220dc.jpg",
    "https://telegra.ph/file/9cc1e4b24bfa13873bd66.jpg",
    "https://telegra.ph/file/792d38bd74b0c3165c11d.jpg",
    "https://telegra.ph/file/e1031e28a4aa4d8bd7c9b.jpg",
    "https://telegra.ph/file/2be9027c55b5ed463fc18.jpg",
    "https://telegra.ph/file/9fd71f8d08158d0cc393c.jpg",
    "https://telegra.ph/file/627105074f0456f42058b.jpg",
    "https://telegra.ph/file/62b712f741382d3c171cd.jpg",
    "https://telegra.ph/file/496651e0d5e4d22b8f72d.jpg",
    "https://telegra.ph/file/6619d0eee2c35e022ee74.jpg",
    "https://telegra.ph/file/f72fcb27c9b1e762d184b.jpg",
    "https://telegra.ph/file/01eac0fe1a722a864d7de.jpg",
    "https://telegra.ph/file/bdcb746fbfdf38f812873.jpg",
    "https://telegra.ph/file/d13e036a129df90651deb.jpg",
    "https://telegra.ph/file/ab6715ce9a63523bd0219.jpg",
    "https://telegra.ph/file/c243f4e80ebf0110f9f00.jpg",
    "https://telegra.ph/file/ff9053f2c7bfb2badc99e.jpg",
    "https://telegra.ph/file/00b9ebbb816285d9a59f9.jpg",
    "https://telegra.ph/file/ad92e1c829d14afa25cf2.jpg",
    ]


@on_message("logo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    randc = random.choice(LOGO_LINKS)
    img = Image.open(io.BytesIO(requests.get(randc).content))
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 350
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 120)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT}  ʙᴀʙʏ🥀')


@on_message("ylogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT} ʙᴀʙʏ🥀')  



@on_message("rlogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="red")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT}  ʙᴀʙʏ🥀')  




@on_message("wlogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="white")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT} ʙᴀʙʏ🥀')  



@on_message("vlogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(65, 105, 225))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="DarkMagenta")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT} ʙᴀʙʏ🥀')

    
@on_message("blogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="blue")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT} ʙᴀʙʏ🥀')  
    
    
    
@on_message("alogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(0,255,255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="aqua")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT} ʙᴀʙʏ🥀')  


@on_message("glogo", allow_stan=True)
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id == OWNER_ID:
     pass
 else:

    if not quew:
       await event.reply('`ᴘʟᴇᴀꜱᴇ ᴀᴅᴅ ᴛᴇxᴛ ᴛᴏ ᴛʜᴇ ɪᴍᴀɢᴇ ʙᴀʙʏ🥀.`')
       return
    else:
       pass
 pesan = await event.reply('`ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʙᴀʙʏ🥀...`')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./MukeshRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    image_widthz, image_heightz = img.size
    pointsize = 500
    fillcolor = "black"
    shadowcolor = "blue"
    fnt = glob.glob("./MukeshRobot/resources/fonts/*")
    randf = random.choice(fnt)
    font = ImageFont.truetype(randf, 800)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_widthz-w)/2, (image_heightz-h)/2), text, font=font, fill=(0,255,255))
    x = (image_widthz-w)/2
    y= ((image_heightz-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="mediumspringgreen")
    fname="LogoMakeBy_IRO.png"
    img.save(fname, "png")
    await tbot.send_file(event.chat_id, file=fname, caption=f"ᴍᴀᴅᴇ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʙᴀʙʏ🥀")         
    await pesan.delete()
    if os.path.exists(fname):
            os.remove(fname)
 except Exception as e:
    await event.reply(f'ᴇʀʀᴏʀ, ʀᴇᴘᴏʀᴛ ᴛᴏ @{SUPPORT_CHAT} ʙᴀʙʏ🥀')  


    

    
    
    
 
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")
