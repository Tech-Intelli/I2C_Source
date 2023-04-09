import os
import telegram


async def send_message_to_bot(photo_path, caption=None):
    chat_id = os.environ['TELEGRAM_PERSONAL_USER']
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
    # Send a message with an image attachment
    with open(photo_path, 'rb') as f:
        await bot.send_photo(chat_id=chat_id, photo=f, caption=caption)
