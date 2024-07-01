"""
Module that extracts trending hashtags

Returns:
    _type_: _description_
"""

import os

from ritetag import RiteTagApi


class TrendingHashtag:
    """Class that extracts trending hashtags"""

    access_token = os.environ["RITEKIT_API_KEY"]
    client = RiteTagApi(access_token)

    def __init__(self):
        def limit_80_percentage_reached(limit):
            message = (
                f"Used {limit.usage}% of API credits. The limit resets on {limit.reset}"
            )
            print(message)

        self.client.on_limit(80, limit_80_percentage_reached)

    def get_trending_hashtags(self, text):
        """Get the trending hash tags

        Returns:
            json: hash tags
        """
        hash_tags = self.client.hashtag_suggestion_for_text(text)
        return hash_tags

    def get_trending_hashtags_from_image(self, image_path):
        """Get the trending hash tags from an image

        Returns:
            json: hash tags
        """
        hash_tags = self.client.hashtag_suggestion_for_image(image_path)
        return hash_tags
