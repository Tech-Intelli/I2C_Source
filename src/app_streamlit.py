"""
Creates a Streamlit powered website
"""

import os
import pathlib
import asyncio
from pathlib import Path
import streamlit as st
import torch
import captioning
from utils.llm_chatbot import LLMChatbot
from inference import InferenceAbstract
from inference.blip2_model import Blip2Model
from inference.llava_model import LlavaModel
from vector_store import initialize_chroma_client
from vector_store import get_chroma_collection
from image_processor.image_compressor import compress_to_webP
from utils.timer import timer_decorator
from utils.stream import stream_text
from utils.generate_gif_placeholder import generate_interim_gif
from video_processor import SceneDetector, SceneSaver
from configuration_manager import ConfigManager


@timer_decorator
def load_model(chroma_collection):
    """
    Loads the model
    """
    app_config = ConfigManager.get_config_manager().get_app_config()
    model_name = app_config.model_selection.model_name
    inference: InferenceAbstract = None
    if model_name == "llava":
        inference: InferenceAbstract = LlavaModel(chroma_collection)
    elif model_name == "blip2":
        inference: InferenceAbstract = Blip2Model(chroma_collection)
    else:
        raise ValueError(f"Model {model_name} not supported")

    if "model_loaded" not in st.session_state:
        inference.load_model()
        st.session_state["model_loaded"] = True

    return inference


# Initialize resources
@st.cache_resource
def initialize_resources():
    """
    Initializes and loads resources for the application.

    This function is decorated with `@st.cache_resource`, which means it will only be executed once per session and its result will be cached for future use.

    Returns:
        Tuple: A tuple containing the following resources:
            - `image_caption_gen` (generate_caption.ImageCaptionGenerator): An instance of the ImageCaptionGenerator class initialized with a chatbot.
            - `chatbot` (generate_caption.Chatbot): An instance of the Chatbot class.
            - `giphy_image` (str): The path to the giphy.gif image file.
            - `chroma_collection` (vector_store.ChromaCollection): A ChromaCollection instance representing the image_caption_vector collection.

    """
    chatbot = LLMChatbot()
    image_caption_gen: captioning.CaptionGenerator = captioning.ImageCaptionGenerator(
        chatbot
    )
    video_caption_generator: captioning.CaptionGenerator = (
        captioning.VideoCaptionGenerator(chatbot, SceneDetector(), SceneSaver())
    )
    giphy_image = os.path.join(Path.cwd(), "../resources", "giphy.gif")
    chroma_collection = get_chroma_collection(
        initialize_chroma_client(), "image_caption_vector"
    )
    inference = load_model(chroma_collection)
    return image_caption_gen, video_caption_generator, giphy_image, inference


@st.cache_data
def save_uploaded_file(uploaded_file, local_directory="temp"):
    """
    Save uploaded file to local directory and return the file path.
    """
    os.makedirs(local_directory, exist_ok=True)
    file_path = os.path.join(local_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


@st.cache_data
def compress_image(uploaded_file):
    """
    Compress the uploaded image to WebP format.
    """
    compressed_image = compress_to_webP(uploaded_file.getvalue())
    compressed_file_name = os.path.splitext(uploaded_file.name)[0] + "_compressed.webp"
    file_path = os.path.join("temp", compressed_file_name)
    with open(file_path, "wb") as f:
        f.write(compressed_image.getbuffer())
    return file_path, compressed_image.getbuffer().nbytes


def process_and_generate_caption(
    file_path,
    file_extension,
    params,
    image_caption_gen,
    video_caption_generator,
    inference,
):
    """
    Process the uploaded file and generate a caption.
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if file_extension in (".png", ".jpeg", ".jpg"):
        caption, compressed_image_path = image_caption_gen.generate_caption(
            "Anywhere on earth",
            file_path,
            params["caption_size"],
            params["context"],
            params["caption_style"],
            params["num_hashtags"],
            params["tone"],
            params["social_media"],
            inference,
        )
        asyncio.run(stream_text(caption))
        st.image(compressed_image_path)
    elif file_extension in (".mp4", ".mov"):
        # TODO : Revisit this for lazy loading of video
        caption = video_caption_generator.generate_caption(
            "Anywhere on earth",
            file_path,
            params["caption_size"],
            params["context"],
            params["caption_style"],
            params["num_hashtags"],
            params["tone"],
            params["social_media"],
            inference,
        )
        asyncio.run(stream_text(caption))
        st.video(file_path)


@timer_decorator
def app():
    """
    The main application that powers Streamlit.
    """
    # Initialize and load resources once
    if "resources" not in st.session_state:
        st.session_state["resources"] = initialize_resources()

    image_caption_gen, video_caption_generator, giphy_image, inference = (
        st.session_state["resources"]
    )

    uploaded_file = st.file_uploader(
        "Upload Image or Video", type=["jpg", "jpeg", "png", "mp4", "mov"]
    )

    if uploaded_file is not None:
        file_extension = pathlib.Path(uploaded_file.name).suffix.lower()

        if file_extension in [".jpg", ".jpeg", ".png"]:
            file_path, file_size = compress_image(uploaded_file)
            st.success("Image uploaded and compressed successfully!")
            st.write(
                f"Compressed image saved at: {file_path} : {file_size / 1024:.2f} kB"
            )
        else:
            file_path = save_uploaded_file(uploaded_file)
            st.success("File uploaded successfully!")

    col1, col2 = st.columns(2)

    with col1:
        caption_size = st.radio(
            "Caption Size",
            options=["small", "medium", "large", "very large", "blog post"],
        )
        caption_style = st.radio(
            "Caption Style",
            options=["cool", "professional", "artistic", "poetic", "poetry"],
        )

    with col2:
        tone = st.radio(
            "Caption Tone",
            options=[
                "casual",
                "humorous",
                "inspirational",
                "conversational",
                "educational",
                "storytelling",
            ],
        )
        social_media = st.radio(
            "Social Media", options=["Instagram", "Facebook", "Twitter", "LinkedIn"]
        )

    context = st.text_area("Write your context here...")
    num_hashtags = st.number_input("How many hashtags do you want to add?", step=1)
    gif_placeholder = generate_interim_gif(giphy_image)
    if st.button("Generate Caption"):
        if uploaded_file is None:
            st.error("Please upload an image or a video.")
        else:
            process_and_generate_caption(
                file_path,
                file_extension,
                {
                    "image_caption_generator": image_caption_gen,
                    "caption_size": caption_size,
                    "caption_style": caption_style,
                    "context": context,
                    "num_hashtags": num_hashtags,
                    "tone": tone,
                    "social_media": social_media,
                },
                image_caption_gen,
                video_caption_generator,
                inference,
            )


if __name__ == "__main__":
    app()
