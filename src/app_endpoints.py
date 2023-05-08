"""
Flask end point for the caption generation
"""
# pylint: disable=E0401
import os
import string
import random
import pathlib
from pathlib import Path
from datetime import datetime
from functools import wraps
from flask import Flask, request, session, jsonify
from generate_caption import Chatbot, ImageCaptionGenerator, VideoCaptionGenerator
from video_scene_detector import SceneDetector, SceneSaver
from aws_s3 import AwsS3
from login.register_user import RegisterUser
from login.authenticate_user import AuthenticateUser
from login.authenticate_user import ForgetPassword

ALLOWED_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mov', 'avi', 'mp4'}
ALLOWED_IMAGE_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_FILE_EXTENSIONS = {'mov', 'avi', 'mp4'}
S3_BUCKET_NAME = 'explaisticbucket'
CHATBOT = Chatbot(os.environ["OPENAI_API_KEY"])
IMAGE_CAPTION_GENERATOR = ImageCaptionGenerator(CHATBOT)
VIDEO_CAPTION_GENERATOR = VideoCaptionGenerator(
    CHATBOT, SceneDetector(), SceneSaver())
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SESSION_SECRET_KEY']


@app.route('/register_user', methods=['POST'])
def register_user():
    """Register a user to the database

    Returns:
        JSON: JSON with response code
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and Password must be provided"}), 400
    reg_user = RegisterUser(email, password)
    response = reg_user.register_user()
    if response == 200:
        return jsonify({"success": "User registered successfully"}), 200
    return jsonify({"error": "User registration failed"}), 500


@app.route('/forget_password', methods=['POST'])
def forget_password():
    """Forget password
    Returns:
        JSON: JSON indicating forget password successful
    """
    data = request.json
    username = data.get('username')
    new_password = data.get('password')

    if not username or not new_password:
        return jsonify({"error": "Email and Password must be provided to reset password"}), 400
    is_password_reset = ForgetPassword(username).forget_password(new_password)
    if is_password_reset:
        return jsonify({"Success": "User's password is reset"}), 200
    return jsonify({"Error": "Password Reset Failed"}), 400


@app.route('/login_user', methods=['POST'])
def login_user():
    """Login user

    Returns:
        JSON: JSON indicating successful or failed login
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and Password must be provided to login"}), 400
    is_user_authenticated = AuthenticateUser(
        email, password).authenticate_user()
    if is_user_authenticated:
        session['email'] = email
        return jsonify({"Success": "User is authenticated and logged in"}), 200
    return jsonify({"Error": "Login failed, please check your email and password"}), 400


def login_required(function):
    """Wrapper function for login_required

    Args:
        f (function): _description_

    Returns:
        decorated_func: _description_
    """
    @wraps(function)
    def decorated_func(*args, **kwargs):
        if 'email' not in session:
            return jsonify({"error": "You must login before using this feature"}), 401
        return function(*args, **kwargs)
    return decorated_func


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


def allowed_file(filename):
    """Checks whether the image file extension is allowed

    Args:
        filename (str): filename of image file

    Returns:
        bool: returns True if image file extension is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    """Uploads a file to the S3 Bucket.

    Returns:
        JSON: if uploaded successfully returns JSON indicating success or failure
    """
    file_path = request.files.get('file')
    if file_path and allowed_file(os.path.basename(file_path.filename)):
        file_name = os.path.basename(file_path.filename)
        file_name = file_name.rsplit('.', 1)[0]
        file_extension = file_path.filename.rsplit('.', 1)[1].lower()
        file_name = generate_random_filename(file_name, file_extension)
        session['file_name'] = file_name
        response = AwsS3.upload_file_object_to_s3(
            file_path.stream, S3_BUCKET_NAME, file_name)
        if response:
            return jsonify({"Uploaded Successfully": True})
        return jsonify({"Upload Failed": False})
    return jsonify({"No File Selected": False})


@app.route('/generate_image_video_caption', methods=['GET'])
@login_required
def generate_image_video_caption():
    """Generates an image caption

    Returns:
        JSON: JSON representation of caption
    """
    file_name = session.get('file_name', None)
    file_save_path = os.path.join(Path.cwd(), file_name)
    AwsS3.download_file_from_s3(
        file_save_path, file_name, S3_BUCKET_NAME)
    caption_size = request.args.get('caption_size', "small")
    context = request.args.get('context', "")
    style = request.args.get('style', 'cool')
    num_hashtags = request.args.get('num_hashtags', 0)
    tone = request.args.get('tone', 'casual')
    social_media = request.args.get('social_media', 'instagram')
    file_extension = pathlib.Path(
        file_save_path).suffix.rsplit('.', 1)[1].lower()
    response_json = None
    if file_extension in ALLOWED_IMAGE_FILE_EXTENSIONS:
        response_json, _ = IMAGE_CAPTION_GENERATOR.generate_caption(
            file_save_path, caption_size, context, style, num_hashtags, tone, social_media)
    elif file_extension in ALLOWED_VIDEO_FILE_EXTENSIONS:
        response_json = VIDEO_CAPTION_GENERATOR.generate_caption(
            file_save_path, caption_size, context, style, num_hashtags, tone, social_media)
    if response_json is not None:
        return jsonify({"Caption": response_json["choices"][0]["message"]["content"]})
    return jsonify({"Caption": "Couldn't find a caption"})


@app.route("/retry_image_video_caption", methods=["GET"])
@login_required
def retry_image_video_caption():
    """Retry captioning
    Returns:
        generate_image_video_caption
    """
    return generate_image_video_caption()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
