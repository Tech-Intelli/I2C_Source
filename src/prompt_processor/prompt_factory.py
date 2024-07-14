from typing import Dict, Any

from prompt_processor.social_media_consts import (
    SocialMedia,
)
from prompt_processor.social_media_strategy import (
    SocialMediaStrategy,
)
from prompt_processor.insta_strategy import InstagramSocialMediaStrategy
from prompt_processor.twitter_strategy import TwitterSocialMediaStrategy
from prompt_processor.linkedin_strategy import LinkedInSocialMediaStrategy
from prompt_processor.facebook_strategy import FacebookSocialMediaStrategy
from prompt_processor.tiktok_strategy import TikTokSocialMediaStrategy


class PromptStrategyFactory:
    """Factory class for creating social media strategy instances."""

    @staticmethod
    def create_strategy(social_media: SocialMedia) -> SocialMediaStrategy:
        """
        Create a strategy instance based on the social media platform.

        Args:
            social_media (SocialMedia): The social media platform.

        Returns:
            SocialMediaStrategy: An instance of the appropriate strategy.

        Raises:
            ValueError: If an unsupported social media platform is provided.
        """

        strategy_map = {
            SocialMedia.INSTAGRAM: InstagramSocialMediaStrategy,
            SocialMedia.TWITTER: TwitterSocialMediaStrategy,
            SocialMedia.LINKEDIN: LinkedInSocialMediaStrategy,
            SocialMedia.FACEBOOK: FacebookSocialMediaStrategy,
            SocialMedia.TIKTOK: TikTokSocialMediaStrategy,
        }

        strategy_class = strategy_map.get(social_media)
        if strategy_class:
            strategy = strategy_class()
            return strategy
        else:
            print(f"Unsupported platform: {social_media}")
            raise ValueError(f"Unsupported social media platform: {social_media}")


class PromptFactory:
    """Factory class for generating prompts."""

    def __init__(self):
        """Initialize the PromptFactory."""
        self.strategy_factory = PromptStrategyFactory()

    def get_prompt(self, params: Dict[str, Any]) -> str:
        """
        Get a prompt based on the provided parameters.

        Args:
            params (Dict[str, Any]): Parameters for prompt generation.

        Returns:
            str: Generated prompt or error message.
        """
        try:
            social_media = SocialMedia(params["social_media"].lower())
            strategy = self.strategy_factory.create_strategy(social_media)
            prompt = strategy.generate_prompt(params)
            return prompt
        except ValueError as e:
            print(f"Invalid social media platform or parameter: {e}")
            return "Error: Invalid social media platform or parameter specified."
        except KeyError as e:
            print(f"Missing required parameter: {e}")
            return f"Error: Missing required parameter: {e}"
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Error: An unexpected error occurred. Please try again later."


"""
# Example usage
if __name__ == "__main__":
    factory = PromptFactory()
    params = {
        "social_media": "tiktok",
        "tone": "casual",
        "style": "storytelling",
        "caption_length": "medium",
        "context": "Earth Day campaign",
        "target_age_group": "millennials and Gen Z",
        "profile_group": "creative_artist",
        "content_type": "carousel",
    }
    prompt = factory.get_prompt(params)
    print(prompt)

    """
