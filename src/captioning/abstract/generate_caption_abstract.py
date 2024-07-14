"""Generates caption for image or reels

Returns:
    str: Caption
"""

from abc import ABC, abstractmethod
from utils.hashtag import Hashtag
from prompt_processor.prompt_factory import PromptFactory


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
        collection=None,
    ):
        pass

    def generate_content_new(
        self,
        imagetotext,
        caption_size,
        context,
        style,
        tone,
        content_type,
        influencer,
        num_hashtags,
        social_media,
    ):
        """
        Generates content using the provided parameters.
        """
        factory = PromptFactory()
        params = {
            "social_media": social_media,
            "tone": tone,
            "style": style,
            "caption_length": caption_size,
            "context": context,
            "visual_description": imagetotext,
            "profile_group": influencer,
            "content_type": content_type,
            "hashtag_limit": num_hashtags,
        }
        prompt = factory.get_prompt(params)

        return prompt

    def _generate_caption_with_hashtags(self, content, num_hashtags):
        """
        Generates a caption with hashtags.
        """
        hashtag = Hashtag(content, self.chatbot)
        stream_caption = self.chatbot.get_response(
            hashtag.generate_hashtagged_caption(num_hashtags), True
        )
        return stream_caption
