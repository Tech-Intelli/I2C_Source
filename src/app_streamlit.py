"""
Creates a Streamlit powered website
"""

# pylint: disable=C0103
# pylint: disable=E0401
# pylint: disable=R0913
# pylint: disable=R0914

import base64
import os
import time
import pathlib
from pathlib import Path
import torch
import streamlit as st
import generate_caption
from video_scene_detector import SceneDetector, SceneSaver
from cached_model import CachedModel
from chromadb_vector_store import initialize_chroma_client
from chromadb_vector_store import get_chroma_collection
from io import StringIO

import signal

def close_server():
    os.kill(os.getpid(), signal.SIGTERM)

if st.button('Exit'):
    close_server()
    
CHATBOT = generate_caption.Chatbot()
IMAGE_CAPTION_GENERATOR = generate_caption.ImageCaptionGenerator(CHATBOT)
GIPHY_IMAGE = os.path.join(Path.cwd(), "resources", "giphy.gif")
CHROMA_COLLECTION = get_chroma_collection(
    initialize_chroma_client(),
    'image_caption_vector')
def load_model():
    """
    Loads the model
    """
    if 'model_loaded' not in st.session_state:
        CachedModel.load_blip2()
        st.session_state['model_loaded'] = True

def generate_image_caption(
        image_path,
        caption_size="small",
        context=None,
        caption_style=None,
        num_hashtags=30,
        tone='casual',
        social_media='Instagram'):
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
        # Do not remove this commented out block. 
        # If needed pass device at the end of the parameter list
        # of generate_caption, default device = 'cpu'

        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("Cuda will be used to generate the caption")
        else:
            device = torch.device("cpu")
            print("CPU will be used to generate the caption")
    """
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    caption, compressed_image_path = IMAGE_CAPTION_GENERATOR.\
        generate_caption(
            "Anywhere on earth",
            image_path,
            caption_size,
            context,
            caption_style,
            num_hashtags,
            tone,
            social_media,
            device,
            CHROMA_COLLECTION)
    return caption, compressed_image_path


def generate_video_caption(
        video_path,
        caption_size="small",
        context=None,
        caption_style=None,
        num_hashtags=30,
        tone='casual',
        social_media='Instagram'):
    """Calls the generated caption's methods to generate video caption

    Args:
        video_path (_type_): path to the video
        caption_size (str, optional): caption size. Defaults to "small".
        context (_type_, optional): user's context. Defaults to None.
        caption_style (_type_, optional): caption's style. Defaults to None.
        num_hashtags (int, optional): number of relevant hashtag. Defaults to 30.

    Returns:
        json: response to generate video caption
        Do not remove this commented out block. 
        If needed pass device at the end of the parameter list
        of generate_caption, default device = 'cpu'
        import torch
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("Cuda will be used to generate the caption")
        else:
            device = torch.device("cpu")
            print("CPU will be used to generate the caption")
    """

    video_caption_generator = generate_caption.VideoCaptionGenerator(
        CHATBOT,
        SceneDetector(),
        SceneSaver()
    )
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    caption = video_caption_generator.generate_caption(
        "Anywhere on earth",
        video_path,
        caption_size,
        context,
        caption_style,
        num_hashtags,
        tone,
        social_media,
        device,
        CHROMA_COLLECTION)
    return caption

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

# pylint: disable=R0915


def stream_text(stream):
    """Generate and display stream text

    Args:
        stream: an iterable streaming API response
    """
    success_stream = st.empty()
    full_text_io = StringIO()

    for chunk in stream:
        message_content = chunk['message']['content'].replace('\n', '<br>')
        full_text_io.write(message_content)
        success_stream.markdown(full_text_io.getvalue(), unsafe_allow_html=True)
        time.sleep(0.03)

    success_stream.success(full_text_io.getvalue())


def app():
    """
    The main application that powers the streamlit.
    """
    load_model()

    uploaded_file = st.file_uploader(
        "Upload Image or Video", type=["jpg", "jpeg", "png", "mp4", "mov"])
    local_directory = 'temp'
    os.makedirs(local_directory, exist_ok=True)
    if uploaded_file is not None:
        file_extension = pathlib.Path(uploaded_file.name).suffix.lower()
        file_path = os.path.join(local_directory, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully!")

    caption_size = st.select_slider(
        'Caption Size',
        options=['small', 'medium', 'large', 'very large', 'blog post'])
    caption_style = st.select_slider(
        'Caption Style',
        options=['cool', 'professional', 'artistic', 'poetic', 'poetry'])
    tone = st.select_slider('Caption tone',
                            options=['casual', 'humorous', 'inspirational',
                                     'conversational', 'educational', 'storytelling'])
    social_media = st.select_slider('Social Media',
                                    options=['Instagram', 'Facebook', 'Twitter', 'LinkedIn'])
    context = st.text_area("Write your context here...")
    num_hashtags = st.number_input(
        "How many hashes do you want to add?", step=1)
    col1, _, _ = st.columns([1, 1, 0.80])
    if col1.button("Generate Caption"):
        if uploaded_file is None:
            st.error("Please upload an image or a video.")
        elif uploaded_file is not None:
            if file_extension in (".png", ".jpeg", ".jpg"):
                gif_placeholder = generate_interim_gif()
                print(f"==== {os.path.abspath(file_path)} ====")
                caption_start_time = time.time()
                caption, compressed_image_path = generate_image_caption(file_path,
                                                                        caption_size,
                                                                        context,
                                                                        caption_style,
                                                                        num_hashtags,
                                                                        tone,
                                                                        social_media)
                caption_end_time = time.time() - caption_start_time
                print(f'Total time taken to to generate a caption is : {caption_end_time} seconds')
                stream_text(caption)
                st.image(compressed_image_path)
                os.remove(file_path)
            elif file_extension in (".mp4", ".mov"):
                gif_placeholder = generate_interim_gif()
                print(f"==== {file_path} ====")
                caption = generate_video_caption(
                    file_path, caption_size, context, caption_style, num_hashtags, tone)
                #gif_placeholder.empty()
                stream_text(caption)
                st.video(file_path)
                os.remove(file_path)


if __name__ == "__main__":
    app()
