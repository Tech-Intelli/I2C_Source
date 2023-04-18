""" Generates caption for image or reels

Returns:
    str: Caption
"""

import os
import shutil
import openai
from cachemodel import CachedModel
from imagecompressor import ImageCompressor
from videoscenedetector import VideoSceneDetector
# pylint: disable=R0903
# pylint: disable=R0913


class Chatbot:
    """
    A class representing a chatbot that interacts with the OpenAI Chat API.

    Attributes:
        api_key (str): The API key for accessing the OpenAI Chat API.
        openai (module): The OpenAI module used for interacting with the
        Chat API.
    """

    def __init__(self, api_key):
        """
        Initializes a new Chatbot instance.

        Args:
            api_key (str): The API key for accessing the OpenAI Chat API.
        """

        self.api_key = api_key
        self.openai = openai

    def get_response(self, content):
        """Sends a message to the OpenAI GPT-3 chat model and returns its
        response.

        Args:
            content (str): The content of the message to be sent.

        Returns:
            dict: A dictionary containing the response from the chat model.
        """

        self.openai.api_key = self.api_key
        response_json = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": content}]
        )
        return response_json


class ImageCaptionGenerator:

    """
    A class that generates captions for images using a chatbot.

    Attributes:
    - chatbot (Chatbot): A chatbot object used for generating captions.

    Methods:
    - __init__(self, chatbot): Constructor method for the
        ImageCaptionGenerator class.
    - generate_caption(self, image_path, caption_size, context, style,
    num_hashtags):
      Generates a caption for an image using the chatbot object.

    """

    def __init__(self, chatbot):
        self.chatbot = chatbot

    def generate_caption(
        self,
            image_path,
            caption_size,
            context,
            style,
            num_hashtags):
        """
        Generates a caption for an image using the chatbot object.

        Args:
        - image_path (str): The path of the image for which the caption is to
            be generated.
        - caption_size (str): The size of the caption to be generated.
        - context (str): The context in which the caption is to be written.
        - style (str): The style in which the caption is to be written.
        - num_hashtags (int): The number of hashtags to be included in the
            caption.

        Returns:
        - response_json (JSON object): The JSON object containing the
            generated caption.
        - compressed_image_path (str): The path of the compressed image used
            for generating the caption.
        """
        compressed_image_path = ImageCompressor.compress(image_path, 10)
        image_pipeline = CachedModel.get_image_caption_pipeline(
            compressed_image_path)
        text = image_pipeline[0]['generated_text']
        caption_size_description = ""
        if caption_size == 'small':
            caption_size_description = "a caption within 2-3 sentences"
        elif caption_size == 'medium':
            caption_size_description = "a caption within 5-7 sentences"
        elif caption_size == 'large':
            caption_size_description = "10-15 sentences"
        elif caption_size == 'very large':
            caption_size_description = "30-50 sentences"
        elif caption_size == 'blog post':
            caption_size_description = "a blog post"
        response_json = None
        if context is not None or context != "":
            context = f'''Write this in the context
            of the following sentence: {context}'''
        content = f''' Write {caption_size_description} for social media
        content for this image in a {style} way and add
        most popular {num_hashtags} hashtags.Don't forget to add some emojis:
        {text}.{context}'''
        response_json = self.chatbot.get_response(content)
        return response_json, compressed_image_path


class VideoCaptionGenerator:
    """
    A class that generates captions for videos using a chatbot.

    Attributes:
    - chatbot (Chatbot): A chatbot object used for generating captions.
    - scene_detector (str): The scene detection algorithm used for extracting
        scenes from the video.
    - scene_saver (str): The scene saving format for the extracted scenes.

    Methods:
    - __init__(self, chatbot, scene_detector, scene_saver):
      Constructor method for the VideoCaptionGenerator class.
    - generate_caption(self, video_path, caption_size, context, style,
        num_hashtags):
      Generates a caption for a video using the chatbot object.
    """

    def __init__(self, chatbot, scene_detector, scene_saver):
        self.chatbot = chatbot
        self.scene_detector = scene_detector
        self.scene_saver = scene_saver

    def generate_caption(self,
                         video_path,
                         caption_size,
                         context, style,
                         num_hashtags):
        """
        Generate a caption for a video using a chatbot.

        Parameters:
        video_path (str): The path to the video file.
        caption_size (str): The desired size of the caption. Valid values are
        'small', 'medium', 'large', 'very large', and 'blog post'.
        context (str): The context in which the caption will be used. Optional.
        style (str): The style in which the caption should be written.
        num_hashtags (int): The number of hashtags to include in the caption.

        Returns:
        dict: A JSON object containing the response from the chatbot.
        """

        scene_dir = "extracted_images"
        vid_scn_detector = VideoSceneDetector(
            video_path,
            self.scene_detector,
            self.scene_saver)
        vid_scn_detector.detect_scenes()
        image_list = os.listdir(scene_dir)
        all_captions = ""
        for each_image in image_list:
            image_pipeline = CachedModel.get_image_caption_pipeline(
                os.path.join(scene_dir, each_image))
            text = image_pipeline[0]['generated_text']
            all_captions += " " + text
        if context is not None or context != "":
            context = f'''Write this in the context
            of the following sentence: {context}'''
        content = f'''Connect these sentences maintaining the sequence
        and rewrite {caption_size} in a {style} way:{all_captions}.
        Add {num_hashtags} hashtags.{context}'''
        response_json = self.chatbot.get_response(content)
        shutil.rmtree(scene_dir, ignore_errors=True)
        return response_json
