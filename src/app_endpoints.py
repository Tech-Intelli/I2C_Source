"""
Flask end point for the caption generation
"""
import os
from flask import Flask, request, jsonify
# pylint: disable=E0401
from generate_caption import Chatbot, ImageCaptionGenerator, VideoCaptionGenerator
from aws_s3 import AwsS3

ALLOWED_IMAGE_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_FILE_EXTENSIONS = {'mov', 'avi', 'mp4'}
S3_BUCKET_NAME = 'explaisticbucket'

app = Flask(__name__)

chatbot = Chatbot(os.environ["OPENAI_API_KEY"])


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
        response = AwsS3.upload_file_object_to_s3(image_path.stream,
                                                  S3_BUCKET_NAME, image_file_name)
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
    if video_path and allowed_video_file(os.path.basename(video_path)):
        video_file_name = os.path.basename(video_path)
        response = AwsS3.upload_file_to_s3(
            video_path, S3_BUCKET_NAME, video_file_name)
        if response:
            return jsonify({"Uploaded Successfully": True})
        return jsonify({"Uploaded Failed": False})
    return jsonify({"No video file selected": False})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
