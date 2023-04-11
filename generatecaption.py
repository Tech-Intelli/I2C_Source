import os
import openai
from cachemodel import CachedModel
from imagecompressor import ImageCompressor


def generate_image_caption(image_dir, image_filename):
    image_path = os.path.join(image_dir, image_filename)
    compressed_image_path = ImageCompressor.compress(image_path, 10)
    image_pipeline = CachedModel.get_image_caption_pipeline(
        compressed_image_path)

    text = image_pipeline[0]['generated_text']

    content_poetry = "Write an instagram caption for this image and add exactly 30 hastags. Don't forget to add some emojis"
    content_poetry = content_poetry + f" : {text}"
    openai.api_key = os.environ["OPENAI_API_KEY"]

    responseJson = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": content_poetry},
        ]
    )
    return responseJson, compressed_image_path
