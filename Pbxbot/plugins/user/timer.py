from pyrogram import Client, filters
from datetime import datetime

# Handler for photo messages
@Client.on_message(filters.self_destruction, group=6)
async def save_photo_with_time(client, message):
    try:
        # Save the photo to a file
        photo_file = await message.download()
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare and send the response message
        response = f"Photo received!\n📅 Time: {timestamp}"
        await message.reply_text(response)
        print(f"Saved photo: {photo_file} at {timestamp}")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text("Something went wrong while processing your photo.")
