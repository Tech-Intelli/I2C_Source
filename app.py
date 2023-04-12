import os
import time
import random
import string
import asyncio

from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request
from sendmessage import send_message_to_bot
from writeresponse import write_response_to_json
from generatecaption import generate_image_caption

app = Flask(__name__)


@app.route('/')
def load():
    return render_template('index.html')


UPLOAD_FOLDER = os.path.join(Path.cwd(), "static", "uploads")
now = datetime.now()
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{random_str}.jpg"


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Get the file from the request
        file = request.files['image']

        # Save the file to the upload folder
        caption = ''
        image_path = os.path.join("uploads", filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        return render_template(
            'index.html', image_path=image_path, caption=caption)
    else:
        return render_template('index.html', caption=caption)


@app.route('/generate', methods=['GET'])
def generate_caption():
    # Get the uploaded file name from the request arguments
    # Generate a caption for the uploaded file
    while True:
        start_time = time.time()
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        responseJson, compressed_image_path = generate_image_caption(
            image_path)
        write_response_to_json(responseJson)
        asyncio.run(send_message_to_bot(
            compressed_image_path,
            responseJson["choices"][0]["message"]["content"]
            ))
        elapsed_time = time.time() - start_time
        # Return the generated caption as a response to the request
        compressed_image_path = os.path.join(
            "uploads", os.path.basename(compressed_image_path))
        return render_template(
            'index.html',
            caption=f'''{responseJson["choices"][0]["message"]["content"]}.
            \n\nThis caption generation took {elapsed_time}''',
            image_path=compressed_image_path)


@app.route('/success')
def success():
    return 'File uploaded successfully!'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
