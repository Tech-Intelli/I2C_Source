"""
Creates a Streamlit powered website
"""

# pylint: disable=C0103
# pylint: disable=E0401
# pylint: disable=R0913
# pylint: disable=R0914

import asyncio
import base64
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
import streamlit as st
import generate_caption
from send_message import send_message_to_bot
from video_scene_detector import SceneDetector, SceneSaver
from write_response import write_response_to_json
from aws_s3 import AwsS3

COMPANY_NAME = "ExplAIstic"

COMPANY_LOGO = os.path.join(Path.cwd(), "resources", "Background.png")
BACKGROUND_IMAGE = os.path.join(Path.cwd(), "resources", "Background.png")
CHATBOT = generate_caption.Chatbot(os.environ["OPENAI_API_KEY"])
IMAGE_CAPTION_GENERATOR = generate_caption.ImageCaptionGenerator(CHATBOT)
GIPHY_IMAGE = os.path.join(Path.cwd(), "resources", "giphy.gif")
S3_BUCKET_NAME = "explaisticbucket"
KEY_NAME = "Test_Image_Explaistic.jpg"


def generate_image_caption(
        image_path,
        caption_size="small",
        context=None,
        caption_style=None,
        num_hashtags=30,
        tone='casual'):
    """Calls the generate_caption's method to generate an image caption

    Args:
        image_path (_type_): path to the image
        caption_size (str, optional): caption size. Defaults to "small".
        context (_type_, optional): user's context. Defaults to None.
        caption_style (_type_, optional): caption's style. Defaults to None.
        num_hashtags (int, optional): number of relevant hashtag. Defaults to 30.
        tone (int, optional): emotional tone. Defaults to casual.

    Returns:
        str: caption
    """
    response_json, compressed_image_path = IMAGE_CAPTION_GENERATOR.\
        generate_caption(
            image_path, caption_size, context, caption_style, num_hashtags, tone)
    caption = response_json["choices"][0]["message"]["content"]
    write_response_to_json(response_json)
    return caption, compressed_image_path


def generate_video_caption(
        video_path,
        caption_size="small",
        context=None,
        caption_style=None,
        num_hashtags=30,
        tone='casual'):
    """Calls the generated caption's methods to generate video caption

    Args:
        video_path (_type_): path to the video
        caption_size (str, optional): caption size. Defaults to "small".
        context (_type_, optional): user's context. Defaults to None.
        caption_style (_type_, optional): caption's style. Defaults to None.
        num_hashtags (int, optional): number of relevant hashtag. Defaults to 30.

    Returns:
        json: response to generate video caption
    """

    video_caption_generator = generate_caption.VideoCaptionGenerator(
        CHATBOT,
        SceneDetector(),
        SceneSaver()
    )
    response_json = video_caption_generator.generate_caption(
        video_path,
        caption_size,
        context,
        caption_style,
        num_hashtags,
        tone)
    caption = response_json["choices"][0]["message"]["content"]
    write_response_to_json(response_json)
    return caption


def send_to_telegram(compressed_image_path, caption):
    """
    Send the caption and compressed image to Telegram

    Args:
        compressed_image_path (str): compressed image path
        caption (str): caption
    """
    asyncio.run(send_message_to_bot(
        compressed_image_path,
        caption,
    ))
    st.success("Message sent.")


def generate_interim_gif():
    """
    Generates gif placeholder

    Returns:
        str: gif placeholder
    """

    gif_placeholder = None
    with open(GIPHY_IMAGE, "rb") as file_gif:
        contents = file_gif.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_gif.close()
        gif_placeholder = st.empty()
        gif_placeholder.markdown(
            f'''<img src="data:image/gif;base64,
                {data_url}" alt="explaistic gif">''',
            unsafe_allow_html=True,
        )
    return gif_placeholder


def app():
    """
    The main application that powers the streamlit.
    """
    st.set_page_config(page_title=COMPANY_NAME, page_icon=COMPANY_LOGO)
    st.image(COMPANY_LOGO)
    st.markdown('<style>img { display: block; margin: auto; }</style>',
                unsafe_allow_html=True)
    st.markdown(f"""
        <style>
            body {{
                background-image: url('{BACKGROUND_IMAGE}');
                background-size: cover;
            }}
        </style>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        with NamedTemporaryFile(dir='.') as temp_file:
            temp_file.write(uploaded_image.getbuffer())
            AwsS3.upload_image_to_s3(temp_file.name, S3_BUCKET_NAME, KEY_NAME)
    uploaded_video = st.file_uploader(
        "Upload Video", type=["mp4", "mov"])

    caption_size = st.select_slider(
        'Caption Size',
        options=['small', 'medium', 'large', 'very large', 'blog post'])
    caption_style = st.select_slider(
        'Caption Style',
        options=['cool', 'professional', 'artistic', 'poetic', 'poetry'])
    tone = st.select_slider('Caption tone',
                            options=['casual', 'humorous', 'inspirational',
                                     'conversational', 'educational', 'storytelling'])
    context = st.text_area("Write your context here...")
    num_hashtags = st.number_input("How many hashes do you want to add?")
    # pylint: disable=W0612
    col1, col2, col3 = st.columns([1, 1, 0.80])
    if col1.button("Generate Caption"):
        if uploaded_image is None:
            st.error("Please upload an image.")
        if uploaded_image is not None and uploaded_video is None:
            gif_placeholder = generate_interim_gif()
            image_save_path = os.path.join(Path.cwd(), KEY_NAME)
            AwsS3.download_image_from_s3(
                image_save_path, KEY_NAME, S3_BUCKET_NAME)
            caption, compressed_image_path = generate_image_caption(
                image_save_path, caption_size, context, caption_style, num_hashtags, tone)
            gif_placeholder.empty()
            st.success(caption)
            st.image(compressed_image_path)
            send_to_telegram(compressed_image_path, caption)
            os.remove(compressed_image_path)
    if col3.button("Generate Video Caption"):
        if uploaded_video is None:
            st.error("Please upload a video.")
        else:
            gif_placeholder = generate_interim_gif()
            with NamedTemporaryFile(dir='.', suffix='.mov | .mp4') as f:
                f.write(uploaded_video.getbuffer())
                caption = generate_video_caption(
                    f.name, caption_size, context, caption_style, num_hashtags, tone)
                gif_placeholder.empty()
                st.success(caption)
                st.video(f.name)


if __name__ == "__main__":
    app()
