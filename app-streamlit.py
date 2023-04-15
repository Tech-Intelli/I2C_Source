import base64
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


def generate_image_caption(image_path, caption_size="small"):
    responseJson, compressed_image_path = IMAGE_CAPTION_GENERATOR.\
        generate_caption(image_path, caption_size)
    caption = responseJson["choices"][0]["message"]["content"]
    return caption, compressed_image_path


def generate_video_caption(video_path, caption_size="small"):
    video_caption_generator = generatecaption.VideoCaptionGenerator(
        CHATBOT,
        SceneDetector(),
        SceneSaver()
    )
    responseJson = video_caption_generator.generate_caption(video_path)
    return responseJson["choices"][0]["message"]["content"]


def generate_interim_gif():
    file_ = open("giphy.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    gif_placeholder = st.empty()
    gif_placeholder.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="explaistic gif">',
        unsafe_allow_html=True,
    )
    return gif_placeholder


def app():
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
    uploaded_video = st.file_uploader(
        "Upload Video", type=["mp4", "mov"])

    caption_size = st.select_slider(
        'Caption Size',
        options=['small', 'medium', 'large', 'very large', 'blog post'])

    col1, col2, col3 = st.columns([1, 1, 0.80])
    if col1.button("Generate Caption"):
        if uploaded_image is None:
            st.error("Please upload an image.")
        if uploaded_image is not None and uploaded_video is None:
            gif_placeholder = generate_interim_gif()
            with NamedTemporaryFile(dir='.', suffix='.jpg |.jepg | .png') as f:
                f.write(uploaded_image.getbuffer())
                caption, compressed_image_path = generate_image_caption(
                    f.name, caption_size)
                os.remove(compressed_image_path)
                gif_placeholder.empty()
                st.success(caption)
                st.image(f.name)
    if col3.button("Generate Video Caption"):
        if uploaded_video is None:
            st.error("Please upload a video.")
        else:
            gif_placeholder = generate_interim_gif()
            with NamedTemporaryFile(dir='.', suffix='.mov | .mp4') as f:
                f.write(uploaded_video.getbuffer())
                caption = generate_video_caption(f.name, caption_size)
                gif_placeholder.empty()
                st.success(caption)
                st.video(f.name)

if __name__ == "__main__":
    app()
