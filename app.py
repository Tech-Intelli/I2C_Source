import os
import time
import openai
import random
import string
import asyncio

from pathlib import Path
from datetime import datetime
from cachemodel import CachedModel
from imagecompressor import ImageCompressor
from sendmessage import send_message_to_bot
from writeresponse import write_response_to_json
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def load():
    return render_template('index.html')


UPLOAD_FOLDER = os.path.join(Path.cwd(), "uploaded")
now = datetime.now()
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{random_str}.jpg"


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Get the file from the request
        file = request.files['image']

        # Save the file to the upload folder
        UPLOAD_FOLDER = os.path.join(Path.cwd(), "uploaded")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        success = 'Image uploaded successfully!'

        return render_template('index.html', success=success)
    else:
        return render_template('index.html')


@app.route('/generate', methods=['GET'])
def generate_caption():
    # Get the uploaded file name from the request arguments
    # Generate a caption for the uploaded file
    while True:
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        start_time = time.time()
        compressed_image_path = ImageCompressor.compress(image_path, 10)
        image_pipeline = CachedModel.get_image_caption_pipeline(
            compressed_image_path)

        text = image_pipeline[0]['generated_text']

        content_poetry = "Write Something for this image and add exactly 30 hastags. Don't forget to add some emojis"
        content_poetry = content_poetry + f" : {text}"
        openai.api_key = os.environ["OPENAI_API_KEY"]

        responseJson = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": content_poetry},
            ]
        )
        elapsed_time = time.time() - start_time
        write_response_to_json(responseJson)
        asyncio.run(send_message_to_bot(
            compressed_image_path, responseJson["choices"][0]["message"]["content"]
            ))
        # Return the generated caption as a response to the request
        return render_template(
            'index.html',
            caption=f'{responseJson["choices"][0]["message"]["content"]}\n\nThis caption generation took {elapsed_time}')


@app.route('/success')
def success():
    return 'File uploaded successfully!'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
