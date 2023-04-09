import os
import telegram

MAX_MESSAGE_LENGTH = 1024


async def send_message_to_bot(photo_path, caption=None):
    chat_id = os.environ['TELEGRAM_PERSONAL_USER']
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
    with open(photo_path, 'rb') as f:
        await bot.send_photo(
            chat_id=chat_id, photo=f, caption=caption[:MAX_MESSAGE_LENGTH])
        for i in range(MAX_MESSAGE_LENGTH, len(caption), MAX_MESSAGE_LENGTH):
            await bot.send_message(
                chat_id=chat_id, text=caption[i:i+MAX_MESSAGE_LENGTH])
