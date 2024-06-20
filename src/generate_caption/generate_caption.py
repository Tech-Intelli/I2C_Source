""" Generates caption for image or reels

    Returns:
        str: Caption
"""

# pylint: disable=R0903
# pylint: disable=R0913
# pylint: disable=E0401
# pylint: disable=R0914
# pylint: disable=E0606
# pylint: disable=W0511
# pylint: disable=W1514
import os
import shutil
import ollama
from cached_model import CachedModel
# from image_compressor import ImageCompressor
from video_scene_detector import VideoSceneDetector

def read_prompt_template(file_path):
    """
    Reads a prompt template from a file.
    """
    with open(file_path, 'r') as file:
        return file.read()

class Chatbot:
    """
    A class representing a chatbot that interacts with the OpenAI Chat API.
    """

    def __init__(self):
        """
        Initializes a new Chatbot instance.
        """

    def get_response(self, content):
        """
        Sends a message to the Ollama llama-3 or phi-3 chat model and returns its
        response.

        Args:
            content (str): The content of the message to be sent.

        Returns:
            dict: A dictionary containing the response from the chat model.
        """

        response = ollama.chat(
            model='llama3',
            messages=[{
                'role': 'user',
                'content': content
            }],
            options={
                'temperature': 0,
                'top_p': 0.9 
            },           
        )
        return response

    def get_stream_response(self, content):
        """Sends a message to the Ollama llama-3 or phi-3 chat model and returns its
        response as a stream.

        Args:
            content (str): The content of the message to be sent.

        Returns:
            dict: A dictionary containing the response from the chat model.
        """
        stream_caption = ollama.chat(
            model='phi3',
            messages=[{
                'role': 'user',
                'content': content
            }],
            stream=True,
            options={
                'temperature': 0,
                'top_p': 0.9 
            },
        )
        return stream_caption

def _get_caption_size(caption_size):
    if caption_size == 'small':
        caption_length = '''Compose a concise 2 to 3 sentence'''
    elif caption_size == 'medium':
        caption_length = '''Compose a concise 5 to 7 sentence'''
    elif caption_size == 'large':
        caption_length = '''Compose a concise 10 to 15 sentence'''
    elif caption_size == 'very large':
        caption_length = '''Compose an extensive 30 to 50 sentence'''
    elif caption_size == 'blog post':
        caption_length = '''Craft an extensive 100 sentence'''
    return caption_length


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
            location,
            image_path,
            caption_size,
            context,
            style,
            num_hashtags,
            tone,
            social_media,
            device='cpu'):
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
        compressed_image_path = image_path  # ImageCompressor.compress(image_path, 10)
        #image_pipeline = CachedModel.get_image_caption_pipeline(
        #    compressed_image_path)
        #text = image_pipeline[0]['generated_text']
        text = CachedModel.get_blip2_image_caption_pipeline(
            compressed_image_path,
            device)
        caption_length = _get_caption_size(caption_size)
        words = caption_length.split()
        only_length = f"{words[-2]} {words[-1]}"
        content = None
        if context is not None or context != "":
            template = read_prompt_template("prompt_template/prompt_with_context.txt")
        else:
            template = read_prompt_template("prompt_template/prompt_without_context.txt")
        content = template.format(
            caption_length=caption_length,
            social_media=social_media,
            location=location,
            text=text,
            style=style,
            context=context,
            tone=tone,
            num_hashtags=num_hashtags,
            only_length=only_length
        )
        stream_caption = self.chatbot.get_stream_response(content)
        return stream_caption, compressed_image_path


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

    def generate_caption(
            self,
            location,
            video_path,
            caption_size,
            context, style,
            num_hashtags,
            tone,
            social_media,
            device='cpu'):
        """
        Generate a caption for a video using a chatbot.

        Parameters:
        video_path (str): The path to the video file.
        caption_size (str): The desired size of the caption. Valid values are
        'small', 'medium', 'large', 'very large', and 'blog post'.
        context (str): The context in which the caption will be used. Optional.
        style (str): The style in which the caption should be written.
        num_hashtags (int): The number of hashtags to include in the caption.
        tone (string): Caption tone.
        Returns:
        dict: A JSON object containing the response from the chatbot.
        """

        scene_dir = "extracted_images"
        os.makedirs(scene_dir, exist_ok=True)
        vid_scn_detector = VideoSceneDetector(
            video_path,
            self.scene_detector,
            self.scene_saver)
        vid_scn_detector.detect_scenes()
        image_list = os.listdir(scene_dir)
        all_captions = ""
        # FIXME: Use parallelism, currently
        #       the code is sequential
        #       and takes a long time to execute
        #       but typical parallelism implementation
        #       does not work, due to model loading
        #       and other issues.
        for each_image in image_list:
            text = CachedModel.get_blip2_image_caption_pipeline(
                os.path.join(scene_dir, each_image),
                device)
            all_captions += " " + text
        content = None
        caption_length = _get_caption_size(caption_size)
        words = caption_length.split()
        only_length = f"{words[-2]} {words[-1]}"
        if context is not None or context != "":
            template = read_prompt_template("prompt_template/prompt_with_context.txt")
        else:
            template = read_prompt_template("prompt_template/prompt_without_context.txt")
        content = template.format(
            caption_length=caption_length,
            social_media=social_media,
            location=location,
            text=text,
            style=style,
            context=context,
            tone=tone,
            num_hashtags=num_hashtags,
            only_length=only_length
        )
        stream_caption = self.chatbot.get_stream_response(content)
        shutil.rmtree(scene_dir, ignore_errors=True)
        return stream_caption
