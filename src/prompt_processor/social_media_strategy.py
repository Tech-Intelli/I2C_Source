from abc import ABC, abstractmethod
from typing import Dict, Any


class SocialMediaStrategy(ABC):
    """
    Abstract base class for social media strategy.

    Attributes:
        platform_data (Dict[str, Any]): Data specific to the social media platform.
    """

    def __init__(self):
        """Initialize the SocialMediaStrategy with platform-specific data."""
        self.platform_data = self.load_platform_data()
        self.template = self.load_template()
        self.influencer_personas = self.load_influencer_personas()

    @abstractmethod
    def generate_prompt(self, params: Dict[str, Any]) -> str:
        """
        Generate a prompt for the social media platform.

        Args:
            params (Dict[str, Any]): Parameters for prompt generation.

        Returns:
            str: Generated prompt.
        """
        pass

    @abstractmethod
    def load_platform_data(self) -> Dict[str, Any]:
        """
        Load platform-specific data.

        Returns:
            Dict[str, Any]: Platform-specific data.
        """
        pass

    def get_tone_style_guide(self, tone: str, style: str) -> str:
        """
        Get tone and style guide based on given parameters.

        Args:
            tone (str): Desired tone for the content.
            style (str): Desired style for the content.

        Returns:
            str: Tone and style guide.
        """
        tone_guides = {
            "casual": "Use conversational language and a friendly approach.",
            "professional": "Maintain a polished and authoritative voice.",
            "humorous": "Incorporate wit and levity, but ensure it's appropriate for the audience.",
            "inspirational": "Use uplifting language and motivational phrases.",
            "educational": "Present information clearly and concisely, focusing on key takeaways.",
            "empathetic": "Show understanding and compassion for your audience's experiences.",
            "enthusiastic": "Express excitement and passion about the topic.",
            "formal": "Use proper language and maintain a serious, business-like tone.",
            "sarcastic": "Use irony and wit, but be cautious not to offend.",
            "nostalgic": "Evoke fond memories and emotions from the past.",
        }
        style_guides = {
            "informative": "Prioritize facts and valuable insights.",
            "storytelling": "Weave a narrative that captures attention and relates to the audience.",
            "persuasive": "Use compelling arguments and calls-to-action.",
            "descriptive": "Paint a vivid picture with words, emphasizing sensory details.",
            "minimalist": "Keep it simple and straightforward, focusing on essential elements.",
            "comparative": "Highlight differences and similarities between concepts or products.",
            "how-to": "Provide step-by-step instructions or tutorials.",
            "listicle": "Present information in an easily digestible numbered or bulleted list format.",
            "behind-the-scenes": "Offer exclusive looks into processes, people, or places.",
            "trending": "Capitalize on current events, popular topics, and viral content in your niche.",
        }
        return f"Tone: {tone_guides.get(tone, '')} Style: {style_guides.get(style, '')}"

    @abstractmethod
    def load_template(self) -> str:
        pass

    @abstractmethod
    def load_influencer_personas(self) -> Dict[str, Dict[str, str]]:
        pass

    def select_influencer_persona(self, params: Dict[str, Any]) -> Dict[str, str]:
        """Select an appropriate influencer persona based on content type and audience."""
        content_type = params.get("profile_group", "").lower()
        personas = self.load_influencer_personas()

        # Directly map content type to persona key
        for persona_key in personas.keys():
            if persona_key in content_type:
                return personas[persona_key]

        # Default to general persona if no match is found
        return personas.get("general", {})

    def generate_visual_description(self, params: Dict[str, Any]) -> str:
        visual_description = params.get("visual_description", "").lower()
        return visual_description

    def get_context(self, params: Dict[str, Any]) -> str:
        context = params.get("context", "").lower()
        return context

    def get_hashtaglimit(self, params: Dict[str, Any]) -> str:
        limit = params.get("hashtag_limit", "")
        return limit

    @abstractmethod
    def add_prompt_engineering_techniques(self, prompt: str) -> str:
        pass

    def get_caption_size(self, caption_size="small"):
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
            "small": "1 to 2 sentences",
            "medium": "2 to 3 sentences",
            "large": "4 to 5 sentences",
        }
        return caption_length_mapping[caption_size]
