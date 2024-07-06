""" Generates caption for image or reels

    Returns:
        str: Caption
"""

from abc import ABC, abstractmethod
from utils.hashtag import Hashtag
from utils.prompt import Prompt


class CaptionGenerator(ABC):
    """
    Abstract base class for generating captions for images or videos.
    """

    def __init__(self, chatbot):
        self.chatbot = chatbot

    @abstractmethod
    def generate_caption(
        self,
        location,
        media_path,
        caption_size,
        context,
        style,
        num_hashtags,
        tone,
        social_media,
        device="cpu",
        collection=None,
    ):
        pass

    def _generate_content(
        self,
        text,
        caption_size,
        context,
        style,
        tone,
        num_hashtags,
        location,
        social_media,
    ):
        """
        Generates content using the provided parameters.
        """
        prompt = Prompt()
        caption_length = prompt._get_caption_size(caption_size)
        words = caption_length.split()
        only_length = f"{words[-2]} {words[-1]}"

        if context is not None or context != "":
            template = prompt._read_prompt_template(
                "../prompt_template/prompt_with_context.txt"
            )
        else:
            template = prompt._read_prompt_template(
                "../prompt_template/prompt_without_context.txt"
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
        return content

    def _generate_caption_with_hashtags(self, content, num_hashtags):
        """
        Generates a caption with hashtags.
        """
        hashtag = Hashtag(content, self.chatbot)
        stream_caption = self.chatbot.get_response(
            hashtag.generate_hashtagged_caption(num_hashtags), True
        )
        return stream_caption
