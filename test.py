import os
import openai
from imagecompressor.imagecompressor import ImageCompressor
from imagecaption.imagecaption import ImageCaptionPipeLine

compressed_image_path = ImageCompressor.compress("test.jpg", 10)
image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
text = image_pipeline("test.jpg")[0]['generated_text']

content_poetry = input("Write what you want ChatGPT to do for you:\n")
content_poetry = content_poetry + f" : {text}"
openai.api_key = os.environ["OPENAI_API_KEY"]

responseJson = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "assistant", "content": content_poetry},
        #{"role": "user", "content": "Who won the world series in 2020?"},
        #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    ]
)

print(responseJson["choices"][0]["message"]["content"])


def writeResponse_to_json(responseJson):
    with open("responseJson.json", "w") as f:
        f.write(str(responseJson))


writeResponse_to_json(responseJson)
