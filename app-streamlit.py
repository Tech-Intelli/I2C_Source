import os
import streamlit as st
import generatecaption
from videoscenedetector.videoscenedetector import SceneDetector, SceneSaver
from tempfile import NamedTemporaryFile

COMPANY_NAME = "ExplAIstic"
COMPANY_LOGO = "Background.png"
BACKGROUND_IMAGE = "Background.png"
CHATBOT = generatecaption.Chatbot(os.environ["OPENAI_API_KEY"])
IMAGE_CAPTION_GENERATOR = generatecaption.ImageCaptionGenerator(CHATBOT)


def generate_image_caption(image_path, caption_size=1):
    responseJson, compressed_image_path = IMAGE_CAPTION_GENERATOR.\
        generate_caption(image_path)
    caption = responseJson["choices"][0]["message"]["content"]
    return caption, compressed_image_path


def generate_video_caption(video_path, caption_size=1):
    video_caption_generator = generatecaption.VideoCaptionGenerator(
        CHATBOT,
        SceneDetector(),
        SceneSaver()
    )
    responseJson = video_caption_generator.generate_caption(video_path)
    return responseJson["choices"][0]["message"]["content"]


def app():
    st.set_page_config(page_title=COMPANY_NAME, page_icon=COMPANY_LOGO)
    st.image(COMPANY_LOGO)
    st.markdown('<style>img { display: block; margin: auto; }</style>', unsafe_allow_html=True)
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
    uploaded_video = st.file_uploader(
        "Upload Video", type=["mp4", "mov"])

    caption_size = st.slider("Caption Size", 1, 2, 3)

    if st.button("Generate Caption"):
        if uploaded_image is not None and uploaded_video is not None:
            st.error("Please upload only one of either an image or a video.")
        if uploaded_image is not None and uploaded_video is None:
            with NamedTemporaryFile(dir='.', suffix='.jpg | \
                                                    .jepg | .png') as f:
                f.write(uploaded_image.getbuffer())
                caption, compressed_image_path = generate_image_caption(
                    f.name, caption_size)
                os.remove(compressed_image_path)
                st.image(f.name)
                st.success(caption)
        elif uploaded_image is None and uploaded_video is not None:
            with NamedTemporaryFile(dir='.', suffix='.mov | .mp4') as f:
                f.write(uploaded_video.getbuffer())
                caption = generate_video_caption(f.name, caption_size)
                st.video(f.name)
                st.success(caption)
        elif uploaded_image is None and uploaded_video is None:
            st.error("Please upload either an image or a video.")


if __name__ == "__main__":
    app()
