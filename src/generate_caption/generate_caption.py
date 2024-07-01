""" Generates caption for image or reels

    Returns:
        str: Caption
"""

import os
import shutil
import ollama
from cached_model import CachedModel
from cached_model import Blip2Model
from video_scene_detector import VideoSceneDetector


def read_prompt_template(file_path):
    """
    Reads a prompt template from a file.
    """
    with open(file_path, "r") as file:
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
            model="phi3",
            messages=[{"role": "user", "content": content}],
            options={"temperature": 1, "top_p": 0.9},
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
            model="phi3",
            messages=[{"role": "user", "content": content}],
            stream=True,
            options={"temperature": 1, "top_p": 0.9},
        )
        return stream_caption


def _get_caption_size(caption_size):
    """
    Get the description of the caption size.

    This function maps a given caption size to a corresponding description string.
    If the provided caption size is not recognized, it returns "Invalid caption size".

    Args:
        caption_size (str): The size of the caption. Can be one of 'small', 'medium',
                            'large', 'very large', or 'blog post'.

    Returns:
        str: The description corresponding to the caption size, or "Invalid caption size"
             if the caption size is not recognized.
    """
    # Dictionary to map caption sizes to their corresponding description
    caption_length_mapping = {
        "small": "Compose a concise 2 to 3 sentences",  # Mapping for 'small' caption size
        "medium": "Compose a concise 5 to 7 sentences",  # Mapping for 'medium' caption size
        "large": "Compose a concise 10 to 15 sentences",  # Mapping for 'large' caption size
        "very large": "Compose an extensive 30 to 50 sentences",  # Mapping for 'very large' caption size
        "blog post": "Craft an extensive 100 sentences",  # Mapping for 'blog post' caption size
    }

    # Retrieve the description based on the caption size provided.
    # If the caption size is not found, return "Compose a concise 2 to 3 sentence".
    return caption_length_mapping.get(
        caption_size, "Compose a concise 2 to 3 sentences"
    )


def parse_hashtags(caption):
    """
    Parses hashtags from the caption and removes them from the original string.

    Args:
    caption (str): The caption containing hashtags.

    Returns:
    tuple: A tuple containing the cleaned caption and a list of hashtags.
    """
    # Split the caption into words
    words = caption.split()
    # Extract hashtags from the words
    hashtags = [word for word in words if word.startswith("#")]
    # Reconstruct the caption without hashtags
    cleaned_caption = " ".join(word for word in words if not word.startswith("#"))
    return cleaned_caption, hashtags


def find_synonyms(word):
    """
    Find synonyms for a given word using Ollama.

    Args:
    word (str): The word to find synonyms for.

    Returns:
    list: A list of synonyms for the given word.
    """
    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": f"Find synonyms for the word '{word}'."}],
        options={"temperature": 0.7, "top_p": 0.9},
    )
    synonyms = response["choices"][0]["text"].strip().split(", ")
    return synonyms


def generate_additional_hashtags(existing_hashtags, num_needed):
    """
    Generate additional hashtags if needed.

    Args:
    existing_hashtags (list): List of existing hashtags.
    num_needed (int): Number of additional hashtags needed.

    Returns:
    list: List of additional hashtags.
    """
    additional_hashtags = []
    # Extract words from existing hashtags (remove the '#')
    words = {hashtag[1:] for hashtag in existing_hashtags}

    for word in words:
        # Find synonyms for each word
        synonyms = find_synonyms(word)
        for synonym in synonyms:
            # Stop if the required number of additional hashtags is reached
            if len(additional_hashtags) >= num_needed:
                break
            # Add the synonym as a hashtag if it's not already in the existing hashtags
            if f"#{synonym}" not in existing_hashtags:
                additional_hashtags.append(f"#{synonym}")

    return additional_hashtags


def generate_hashtaged_caption(caption, num_tags):
    """
    Generate a string of hashtags from a caption.

    Parameters:
    caption (str): The caption from which to generate hashtags.
    num_tags (int): The desired number of hashtags to generate.

    Returns:
    str: A string containing the original caption and the generated hashtags.
    """
    MAX_HASHTAGS = 30
    if num_tags > MAX_HASHTAGS:
        num_tags = MAX_HASHTAGS

    # Parse hashtags from the caption
    cleaned_caption, hashtags = parse_hashtags(caption)
    num_existing_tags = len(hashtags)

    # Generate additional hashtags if needed
    if num_existing_tags < num_tags:
        additional_hashtags = generate_additional_hashtags(
            hashtags, num_tags - num_existing_tags
        )
        hashtags.extend(additional_hashtags)

    # Ensure the number of hashtags does not exceed the maximum limit
    hashtags = hashtags[:num_tags]

    # Construct the result with a line break between the caption and hashtags
    return f"{cleaned_caption}\n\n{' '.join(hashtags)}"


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
        device="cpu",
        collection=None,
    ):
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
        compressed_image_path = image_path
        cachedModel: CachedModel = Blip2Model(collection)
        text = cachedModel.get_image_caption_pipeline(image_path)
        caption_length = _get_caption_size(caption_size)
        words = caption_length.split()
        only_length = f"{words[-2]} {words[-1]}"
        content = None
        if context is not None or context != "":
            template = read_prompt_template("prompt_template/prompt_with_context.txt")
        else:
            template = read_prompt_template(
                "prompt_template/prompt_without_context.txt"
            )
        content = template.format(
            caption_length=caption_length,
            social_media=social_media,
            location=location,
            text=text,
            style=style,
            context=context,
            tone=tone,
            num_hashtags=num_hashtags,
            only_length=only_length,
        )

        stream_caption = self.chatbot.get_stream_response(
            generate_hashtaged_caption(content, num_hashtags)
        )
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
        context,
        style,
        num_hashtags,
        tone,
        social_media,
        device="cpu",
        collection=None,
    ):
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
            video_path, self.scene_detector, self.scene_saver
        )
        vid_scn_detector.detect_scenes()
        image_list = os.listdir(scene_dir)
        all_captions = ""
        # FIXME: Use parallelism, currently
        #       the code is sequential
        #       and takes a long time to execute
        #       but typical parallelism implementation
        #       does not work, due to model loading
        #       and other issues.
        cachedModel: CachedModel = Blip2Model(collection)
        for each_image in image_list:
            text = cachedModel.get_image_caption_pipeline(
                os.path.join(scene_dir, each_image)
            )
            all_captions += " " + text
        content = None
        caption_length = _get_caption_size(caption_size)
        words = caption_length.split()
        only_length = f"{words[-2]} {words[-1]}"
        if context is not None or context != "":
            template = read_prompt_template("prompt_template/prompt_with_context.txt")
        else:
            template = read_prompt_template(
                "prompt_template/prompt_without_context.txt"
            )
        content = template.format(
            caption_length=caption_length,
            social_media=social_media,
            location=location,
            text=text,
            style=style,
            context=context,
            tone=tone,
            num_hashtags=num_hashtags,
            only_length=only_length,
        )
        stream_caption = self.chatbot.get_stream_response(content)
        shutil.rmtree(scene_dir, ignore_errors=True)
        return stream_caption
