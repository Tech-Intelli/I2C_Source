"""
Flask end point for the caption generation
"""
# pylint: disable=E0401
import os
import string
import random
from pathlib import Path
from datetime import datetime
from flask import Flask, request, session, jsonify
from generate_caption import Chatbot, ImageCaptionGenerator, VideoCaptionGenerator
from video_scene_detector import SceneDetector, SceneSaver
from aws_s3 import AwsS3

ALLOWED_IMAGE_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_FILE_EXTENSIONS = {'mov', 'avi', 'mp4'}
S3_BUCKET_NAME = 'explaisticbucket'
CHATBOT = Chatbot(os.environ["OPENAI_API_KEY"])
IMAGE_CAPTION_GENERATOR = ImageCaptionGenerator(CHATBOT)
VIDEO_CAPTION_GENERATOR = VideoCaptionGenerator(
    CHATBOT, SceneDetector(), SceneSaver())
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SESSION_SECRET_KEY']


def generate_random_filename(filename, extension):
    """Generate a random filename

    Args:
        filename (str): Filename to generate a random filename

    Returns:
        str: random filename
    """
    now = datetime.now()
    random_str = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=8))
    filename = filename.split('.')[0]
    filename = filename + \
        f"{now.strftime('%Y%m%d_%H%M%S')}_{random_str}.{extension}"
    return filename


def allowed_image_file(filename):
    """Checks whether the image file extension is allowed

    Args:
        filename (str): filename of image file

    Returns:
        bool: returns True if image file extension is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_FILE_EXTENSIONS


def allowed_video_file(filename):
    """Checks whether the video file extension is allowed

    Args:
        filename (str): _description_

    Returns:
        bool: returns True if the video file extension is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_FILE_EXTENSIONS


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Uploads an image to the S3 Bucket.

    Returns:
        JSON: if uploaded successfully returns JSON indicating sucess or failure
    """
    image_path = request.files.get('image')
    if image_path and allowed_image_file(os.path.basename(image_path.filename)):
        image_file_name = os.path.basename(image_path.filename)
        file_name = image_file_name.rsplit('.', 1)[0]
        file_extension = image_file_name.rsplit('.', 1)[1].lower()
        image_file_name = generate_random_filename(file_name, file_extension)
        session['image_file_name'] = image_file_name
        response = AwsS3.upload_file_object_to_s3(
            image_path.stream, S3_BUCKET_NAME, image_file_name)
        if response:
            return jsonify({"Uploaded Successfully": True})
        return jsonify({"Upload Failed": False})
    return jsonify({"No Image File Selected": False})


@app.route('/upload_video', methods=['POST'])
def upload_video():
    """Uploads a video to the S3 bucket.

    Returns:
        JSON: if uploaded successfully returns JSON indicating success or failure
    """
    video_path = request.files.get('video')
    if video_path and allowed_video_file(os.path.basename(video_path.filename)):
        video_file_name = os.path.basename(video_path.filename)
        file_name = video_file_name.rsplit('.', 1)[0]
        file_extension = video_file_name.rsplit('.', 1)[1].lower()
        video_file_name = generate_random_filename(file_name, file_extension)
        session['video_file_name'] = video_file_name
        response = AwsS3.upload_file_object_to_s3(
            video_path, S3_BUCKET_NAME, video_file_name)
        if response:
            return jsonify({"Uploaded Successfully": True})
        return jsonify({"Uploaded Failed": False})
    return jsonify({"No video file selected": False})


@app.route('/generate_image_caption', methods=['GET'])
def generate_image_caption():
    """Generates an image caption

    Returns:
        JSON: JSON representation of caption
    """
    image_file_name = session.get('image_file_name', None)
    image_save_path = os.path.join(Path.cwd(), image_file_name)
    AwsS3.download_image_from_s3(
        image_save_path, image_file_name, S3_BUCKET_NAME)
    caption_size = request.args.get('caption_size', "small")
    context = request.args.get('context', "")
    style = request.args.get('style', 'cool')
    num_hashtags = request.args.get('num_hashtags', 0)
    tone = request.args.get('tone', 'casual')
    social_media = request.args.get('social_media', 'instagram')
    response_json, _ = IMAGE_CAPTION_GENERATOR.generate_caption(
        image_save_path, caption_size, context, style, num_hashtags, tone, social_media)
    if response_json is not None:
        return jsonify({"Caption": response_json["choices"][0]["message"]["content"]})
    return jsonify({"Caption": "Couldn't find a caption"})


@app.route('/generate_video_caption', methods=['GET'])
def generate_video_caption():
    """Generates a video caption

    Returns:
        JSON: JSON representation of caption
    """
    video_file_name = session.get('video_file_name', None)
    video_save_path = os.path.join(Path.cwd(), video_file_name)
    AwsS3.download_image_from_s3(
        video_save_path, video_file_name, S3_BUCKET_NAME)
    caption_size = request.args.get('caption_size', "small")
    context = request.args.get('context', "")
    style = request.args.get('style', 'cool')
    num_hashtags = request.args.get('num_hashtags', 0)
    tone = request.args.get('tone', 'casual')
    social_media = request.args.get('social_media', 'instagram')
    response_json = VIDEO_CAPTION_GENERATOR.generate_caption(
        video_save_path, caption_size, context, style, num_hashtags, tone, social_media)
    if response_json is not None:
        return jsonify({"Caption": response_json["choices"][0]["message"]["content"]})
    return jsonify({"Caption": "Couldn't find a caption"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
