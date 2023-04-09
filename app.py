import os
import openai
import asyncio
from imagecompressor import ImageCompressor
from cachemodel import CachedModel
from sendmessage import send_message_to_bot
from writeresponse import write_response_to_json


while True:
    image_path = input("Please provide an image file:\n")
    compressed_image_path = ImageCompressor.compress(image_path, 10)
    image_pipeline = CachedModel.get_image_caption_pipeline(
        compressed_image_path)

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

    write_response_to_json(responseJson)
    asyncio.run(send_message_to_bot(
        compressed_image_path, responseJson["choices"][0]["message"]["content"]
        ))
