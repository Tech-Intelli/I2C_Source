''''
"""
Create the flask based website
"""
import os
import time
import random
import string
import asyncio

from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request
from send_message.send_message import send_message_to_bot
from write_response.write_response import write_response_to_json
from generate_caption.generate_caption import Chatbot, ImageCaptionGenerator

UPLOAD_FOLDER = os.path.join(Path.cwd(), "static", "uploads")
now = datetime.now()
random_str = ''.join(random.choices(
    string.ascii_lowercase + string.digits, k=8))
filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{random_str}.jpg"

app = Flask(__name__)


@app.route('/')
def load():
    """
    renders the template
    """

    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    """
    Uploads the image
    """

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
    """
    Get the uploaded file name from the request arguments
    Generate a caption for the uploaded file
    """

    while True:
        start_time = time.time()
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        chatbot = Chatbot(os.environ["OPENAI_API_KEY"])
        image_caption_generator = ImageCaptionGenerator(chatbot)
        response_json, compressed_image_path = image_caption_generator.\
            generate_caption(image_path, "small", "", 10)
        write_response_to_json(response_json)
        asyncio.run(send_message_to_bot(
            compressed_image_path,
            response_json["choices"][0]["message"]["content"]
        ))
        elapsed_time = time.time() - start_time
        compressed_image_path = os.path.join(
            "uploads", os.path.basename(compressed_image_path))
        return render_template(
            'index.html',
            caption=f"""{response_json["choices"][0]["message"]["content"]}.
            \n\nThis caption generation took {elapsed_time}""",
            image_path=compressed_image_path)


@app.route('/success')
def success():
    return 'File uploaded successfully!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
'''
