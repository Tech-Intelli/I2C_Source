"""
Flask end point for the caption generation
"""
# pylint: disable=E0401
# pylint: disable=R0914
import os
import string
import random
import uuid
from datetime import datetime
from functools import wraps
import jwt
import requests
from PIL import Image
from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_session import Session
from generate_caption import Chatbot, ImageCaptionGenerator, VideoCaptionGenerator
from video_scene_detector import SceneDetector, SceneSaver
from aws_s3 import AwsS3
from login.register_user import RegisterUser
from login.register_user import VerifyEmail
from login.authenticate_user import AuthenticateUser
from login.authenticate_user import AuthenticateAsGuest
from login.authenticate_user import ForgetPassword
from login.database import get_user_id

INSTAGRAM_CLIENT_ID = os.environ.get('INSTAGRAM_CLIENT_ID')
INSTAGRAM_CLIENT_SECRET = os.environ.get('INSTAGRAM_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:9000/auth'
AUTH_URL = 'https://api.instagram.com/oauth/authorize'
TOKEN_URL = 'https://api.instagram.com/oauth/access_token'
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
app.config['SESSION_TYPE'] = 'filesystem'
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True
)
Session(app)
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": "*",
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE"]
    }
})

@app.route('/health', methods=['GET'])
def health():
    """Basic health check
    Returns:
        200
    """
    return "Healthy", 200

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


@app.route('/verify/<unique_id>', methods=['GET'])
def verify(unique_id):
    """Verifies a user

    Returns:
        JSON: JSON with response code
    """
    response = VerifyEmail.verify_email(unique_id)
    if response:
        return jsonify({"success": "User verified successfully"}), 200
    return jsonify({"Failure": "User cannot be verified"}), 400


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
    authenticate_user = AuthenticateUser(email, password)
    is_user_authenticated = authenticate_user.authenticate_user()
    if is_user_authenticated:
        session['email'] = email
        user_id = get_user_id(email)
        session['user_id'] = user_id
        token = authenticate_user.generate_auth_token(user_id)
        return jsonify({"Success": "User is authenticated and logged in", "token": token}), 200
    return jsonify({"Error": """Login failed, please check your email and password.
                    Please make sure you have verified your email address."""}), 400

# pylint: disable=W0511
# fixme:This should be handled directly in the front-end


@app.route('/login_as_guest', methods=['POST'])
def login_as_guest():
    """ login as guest
    Returns:
        JSON: JSON indicating successful or failed login as guest
    """
    session_id = str(uuid.uuid4())
    session['guest_id'] = session_id
    auth_as_guest_user = AuthenticateAsGuest()
    token = auth_as_guest_user.generate_auth_token_guest(session_id)
    return jsonify({
        "Success": "User logged in successfully as a guest",
        "guest_id": session_id,
        "token": token}), 200


@app.route('/logout_user', methods=['POST'])
def logout_user():
    """ logout user
    Returns:
        JSON: JSON indicating if user successfully logged out.
    """
    session.clear()
    return jsonify({"Success": "User Successfully Logged Out"}), 200


@app.route('/insta_login')
def insta_login():
    """Instagram link
    """
    auth_url = f'''{AUTH_URL}?client_id={INSTAGRAM_CLIENT_ID}&
redirect_uri={REDIRECT_URI}&scope=user_profile&response_type=code'''
    return f'<a href="{auth_url}">Log in with Instagram</a>'


@app.route('/insta_auth')
def instagram_auth():
    """Authentication using Instagram

    Returns:
        JSON Response: JSON response indicating authentication success.
    """
    code = request.args.get('code')
    if not code:
        return 'Error: Authorization code not found.', 400

    data = {
        'client_id': INSTAGRAM_CLIENT_ID,
        'client_secret': INSTAGRAM_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code,
    }
    response = requests.post(TOKEN_URL, data=data, timeout=30)
    if response.status_code != 200:
        return jsonify({f'Error: {response.json().get("error_message")}'}), 400

    user_id = response.json().get('user_id')
    session['email'] = user_id
    return jsonify({f'Logged in successfully! User ID: {user_id}'})


def login_required(function):
    """Wrapper function for login_required

    Args:
        function (function): _description_

    Returns:
        decorated_func: Decode payload
    """
    @wraps(function)
    def decorated_func(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token, os.environ['AUTH_SECRET_KEY'], algorithms=['HS256'])
            request.user_id = payload['user_id']
            request.email = payload['email']
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403
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
    session['address'] = 'Somewhere on Earth'
    if request.form.get('address') is not None:
        session['address'] = request.form.get('address')
    if file_path and allowed_file(os.path.basename(file_path.filename)):
        file_name = os.path.basename(file_path.filename)
        file_extension = file_name.rsplit('.', 1)[1].lower()
        file_name = file_name.rsplit('.', 1)[0]
        file_name = generate_random_filename(file_name, file_extension)
        session['file_name'] = f'''{request.user_id}/{file_name}'''
        response = AwsS3.upload_file_object_to_s3(
            file_path.stream, request.user_id, S3_BUCKET_NAME, file_name)
        if response:
            return jsonify({
                "Uploaded Successfully": True,
                "file_name": session['file_name'],
                "address": session['address']})
        return jsonify({"Upload Failed": False})
    return jsonify({"No File Selected": False})

@app.route('/generate_image_video_caption', methods=['GET'])
@login_required
def generate_image_video_caption():
    """Generates an image caption

    Returns:
        JSON: JSON representation of caption
    """
    auth_header = request.headers.get('Authorization')
    # pylint: disable=W0612
    token = ''
    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        token = ''
    file_name = request.args.get('file_name')
    if file_name.startswith('"') and file_name.endswith('"'):
        file_name = file_name[1:-1]
    if file_name is None:
        return jsonify({"Error": "Cannot fetch file from session."}), 500
    caption_size = request.args.get('caption_size', 'small')
    context = request.args.get('context', '')
    style = request.args.get('style', 'cool')
    num_hashtags = request.args.get('num_hashtags', 0)
    tone = request.args.get('tone', 'casual')
    social_media = request.args.get('social_media', 'instagram')
    location = request.args.get('address', 'Somewhere on Earth')
    presigned_url = AwsS3.create_presigned_url(S3_BUCKET_NAME, file_name)
    has_image_file_extension = False
    has_video_file_extension = False
    video_file_extension = ""
    for any_image_extension in ALLOWED_IMAGE_FILE_EXTENSIONS:
        if any_image_extension in presigned_url:
            has_image_file_extension = True
            break
    for any_video_extension in ALLOWED_VIDEO_FILE_EXTENSIONS:
        if any_video_extension in presigned_url:
            has_video_file_extension = True
            video_file_extension = any_video_extension
            break
    response_json = None
    # pylint: disable=W3101
    if has_image_file_extension:
        file_save_path = Image.open(requests.get(presigned_url, stream=True).raw)
        response_json, _ = IMAGE_CAPTION_GENERATOR.generate_caption(
            location,
            file_save_path,
            caption_size,
            context,
            style,
            num_hashtags,
            tone,
            social_media)
    elif has_video_file_extension:
        file_name_only = file_name.split('/')[1]
        video_file_path = generate_random_filename(file_name_only, video_file_extension)
        req = requests.get(presigned_url, stream=True)
        if req.status_code == 200:
            with open(video_file_path, 'wb') as file:
                file.write(req.content)
        response_json = VIDEO_CAPTION_GENERATOR.generate_caption(
            location,
            video_file_path,
            caption_size,
            context,
            style,
            num_hashtags,
            tone,
            social_media)
        os.remove(video_file_path)
    if response_json is not None:
        return jsonify({
            "Caption": response_json["choices"][0]["message"]["content"],
            "File_URL": presigned_url})
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
