import asyncio
import base64
import os
import time
import pathlib
from pathlib import Path
import tempfile
import streamlit as st
import generate_caption
from send_message import send_message_to_bot
from video_scene_detector import SceneDetector, SceneSaver
from write_response import write_response_to_json
from aws_s3 import AwsS3
#from trending_hashtag import TrendingHashtag
from dotenv import load_dotenv
COMPANY_NAME = "ExplAIstic"

COMPANY_LOGO = os.path.join(Path.cwd(), "resources", "Background.png")
BACKGROUND_IMAGE = os.path.join(Path.cwd(), "resources", "Background.png")
CHATBOT = generate_caption.Chatbot(os.getenv("OPENAI_API_KEY"))
IMAGE_CAPTION_GENERATOR = generate_caption.ImageCaptionGenerator(CHATBOT)

response_json, compressed_image_path = IMAGE_CAPTION_GENERATOR.\
    generate_caption(
        "Anywhere on earth",
        "C:\\Users\\dasdi\\Desktop\\5.JPEG",
        "small",
        "",
        "cool",
        30,
        "casual",
        "Instagram")
caption = response_json["choices"][0]["message"]["content"]
print(caption)