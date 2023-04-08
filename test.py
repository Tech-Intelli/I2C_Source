import os
import openai
import warnings
import telegram
import asyncio
from imagecompressor.imagecompressor import ImageCompressor
from cachemodel.diskcachedmodel import get_image_caption_pipeline

warnings.filterwarnings("ignore")


image_path = input("Please provide an image file:\n")
compressed_image_path = ImageCompressor.compress(image_path, 10)
image_pipeline = get_image_caption_pipeline(compressed_image_path)

text = image_pipeline[0]['generated_text']

content_poetry = input("Write what you want ChatGPT to do for you:\n\n")
content_poetry = content_poetry + f" : {text}"
openai.api_key = os.environ["OPENAI_API_KEY"]

responseJson = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "assistant", "content": content_poetry},
    ]
)


def writeResponse_to_json(responseJson):
    with open("responseJson.json", "a") as f:
        f.write(str(responseJson))
    with open("output.txt", "a") as f:
        f.write(responseJson["choices"][0]["message"]["content"])


writeResponse_to_json(responseJson)
caption = responseJson["choices"][0]["message"]["content"]


async def something(photo_path, caption=None):
    chat_id = os.environ['TELEGRAM_PERSONAL_USER']
    bot = telegram.Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
    # Send a message with an image attachment
    with open(photo_path, 'rb') as f:
        await bot.send_photo(chat_id=chat_id, photo=f, caption=caption)


photo_path = image_path

asyncio.run(something(photo_path, caption))
