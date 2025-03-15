import os
import io
import random
import glob
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import Message
from . import Config, on_message

LOGO_LINKS = [
    "https://telegra.ph/file/d1838efdafce9fe611d0c.jpg",
    "https://telegra.ph/file/c1ff2d5ec5e1b5bd1b200.jpg",
    "https://telegra.ph/file/08c5fbe14cc4b13d1de05.jpg",
    "https://telegra.ph/file/66614a049d74fe2a220dc.jpg",
]

# Global Function to Generate Logo
async def generate_text_logo(text, stroke_color, background=None):
    """Generate a logo with the given text and stroke color."""
    try:
        # Random background image (if provided)
        if background:
            img = Image.open(background)
        else:
            randc = random.choice(LOGO_LINKS)
            img = Image.open(io.BytesIO(requests.get(randc).content))

        draw = ImageDraw.Draw(img)
        image_width, image_height = img.size

        # Select a random font
        font_files = glob.glob("./Pbxbot/resources/fonts/*")
        if not font_files:
            raise FileNotFoundError("No fonts found in the specified directory.")
        randf = random.choice(font_files)
        font = ImageFont.truetype(randf, 120)

        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        w = text_bbox[2] - text_bbox[0]
        h = text_bbox[3] - text_bbox[1] + int((text_bbox[3] - text_bbox[1]) * 0.21)

        # Apply text
        x, y = (image_width - w) / 2, (image_height - h) / 2
        draw.text((x, y), text, font=font, fill="white", stroke_width=2, stroke_fill=stroke_color)

        # Save and return filename
        fname = "Generated_Logo.png"
        img.save(fname, "png")
        return fname
    except Exception as e:
        print(f"Error generating logo: {e}")
        return None

# Command Handler
async def handle_logo_command(client, message, stroke_color, background=None):
    """Handle all logo commands dynamically."""
    try:
        quew = message.text.split(' ', 1)[1] if ' ' in message.text else None
        if not quew:
            await message.reply_text('Please provide text for the logo.')
            return
        
        msg = await message.reply_text('Processing...')
        fname = await generate_text_logo(quew, stroke_color, background)

        if fname:
            await message.reply_photo(photo=fname, caption="Logo Generated!")
            os.remove(fname)
        else:
            await message.reply_text("An error occurred while generating the logo.")
        
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
        print(f"Error in logo command: {e}")

# Logo Commands
@on_message("logo", allow_stan=True)
async def logo(client: Client, message: Message):
    await handle_logo_command(client, message, "black")

@on_message("ylogo", allow_stan=True)
async def ylogo(client: Client, message: Message):
    await handle_logo_command(client, message, "yellow", "./Pbxbot/resources/fonts/blackbg.jpg")

@on_message("rlogo", allow_stan=True)
async def rlogo(client: Client, message: Message):
    await handle_logo_command(client, message, "red", "./Pbxbot/resources/fonts/blackbg.jpg")

@on_message("wlogo", allow_stan=True)
async def wlogo(client: Client, message: Message):
    await handle_logo_command(client, message, "white", "./Pbxbot/resources/fonts/blackbg.jpg")

@on_message("vlogo", allow_stan=True)
async def vlogo(client: Client, message: Message):
    await handle_logo_command(client, message, "DarkMagenta", "./Pbxbot/resources/fonts/blackbg.jpg")

@on_message("blogo", allow_stan=True)
async def blogo(client: Client, message: Message):
    await handle_logo_command(client, message, "blue", "./Pbxbot/resources/fonts/blackbg.jpg")

@on_message("alogo", allow_stan=True)
async def alogo(client: Client, message: Message):
    await handle_logo_command(client, message, "aqua", "./Pbxbot/resources/fonts/blackbg.jpg")

@on_message("glogo", allow_stan=True)
async def glogo(client: Client, message: Message):
    await handle_logo_command(client, message, "mediumspringgreen", "./Pbxbot/resources/fonts/blackbg.jpg")
