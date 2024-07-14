from typing import Dict, Any
from prompt_processor.social_media_strategy import SocialMediaStrategy


class InstagramSocialMediaStrategy(SocialMediaStrategy):
    """Strategy class for Instagram."""

    def __init__(self):
        super().__init__()

    def load_template(self) -> str:
        """Load the Instagram prompt template from a file."""
        with open("prompt_processor/templates/insta_template.txt", "r") as file:
            return file.read()

    def load_platform_data(self) -> Dict[str, Any]:
        """Load Instagram-specific data."""
        return {
            "max_length": 2200,
            "hashtag_limit": 30,
            "best_practices": "Use a mix of relevant hashtags, engage with storytelling, and use emojis sparingly.",
            "seo_tips": "Use relevant keywords in your caption.",
            "content_types": ["IMAGE", "VIDEO", "CAROUSEL"],
        }

    def load_influencer_personas(self) -> Dict[str, Dict[str, str]]:
        """Load predefined influencer personas."""
        return {
            "lifestyle": {
                "niche": "lifestyle and personal development",
                "style_description": "inspirational and relatable",
                "content_focus": "day-in-the-life and motivational content",
            },
            "fashion": {
                "niche": "fashion and personal style",
                "style_description": "trendy and expressive",
                "content_focus": "outfit inspiration and fashion tips",
            },
            "food": {
                "niche": "culinary arts and food culture",
                "style_description": "descriptive and mouth-watering",
                "content_focus": "recipe sharing and restaurant reviews",
            },
            "travel": {
                "niche": "travel and adventure",
                "style_description": "vivid and wanderlust-inducing",
                "content_focus": "destination highlights and travel tips",
            },
            "fitness": {
                "niche": "fitness and wellness",
                "style_description": "motivational and informative",
                "content_focus": "workout routines and health advice",
            },
            "beauty": {
                "niche": "beauty and skincare",
                "style_description": "glamorous and tutorial-style",
                "content_focus": "makeup looks and skincare routines",
            },
            "tech": {
                "niche": "technology and gadgets",
                "style_description": "tech-savvy and analytical",
                "content_focus": "product reviews and tech news",
            },
            "parenting": {
                "niche": "parenting and family life",
                "style_description": "supportive and humorous",
                "content_focus": "parenting tips and family activities",
            },
            "business": {
                "niche": "entrepreneurship and career development",
                "style_description": "professional and motivational",
                "content_focus": "business advice and success stories",
            },
            "art": {
                "niche": "art and creativity",
                "style_description": "artistic and expressive",
                "content_focus": "artwork showcases and creative processes",
            },
            "sustainability": {
                "niche": "eco-friendly living and sustainability",
                "style_description": "environmentally conscious and informative",
                "content_focus": "eco-tips and sustainable product reviews",
            },
            "petcare": {
                "niche": "pet care and animal lovers",
                "style_description": "warm and educational",
                "content_focus": "pet care advice and cute animal content",
            },
            "gaming": {
                "niche": "gaming and esports",
                "style_description": "enthusiastic and entertaining",
                "content_focus": "game reviews and streaming highlights",
            },
            "books": {
                "niche": "literature and book reviews",
                "style_description": "thoughtful and analytical",
                "content_focus": "book recommendations and reading challenges",
            },
            "music": {
                "niche": "music and entertainment",
                "style_description": "upbeat and trend-setting",
                "content_focus": "music reviews and artist spotlights",
            },
            "general": {
                "niche": "visual content and lifestyle",
                "style_description": "aesthetic and captivating",
                "content_focus": "beautiful photos, lifestyle inspiration, and visual storytelling",
            },
        }

    def add_prompt_engineering_techniques(self, prompt: str) -> str:
        """Apply prompt engineering techniques to improve LLM output for Instagram."""
        techniques = [
            "Create a visually descriptive caption that complements the image or video.",
            "Use a mix of short and long sentences for rhythm and easy readability.",
            "Incorporate storytelling elements to engage the audience and encourage longer view times.",
            "Add a clear call-to-action that encourages engagement (likes, comments, saves, or shares).",
            "Use emojis sparingly to add personality and break up text, but don't overdo it.",
            "Mention other accounts when relevant to increase reach and collaboration opportunities.",
            "Consider adding 'hidden' hashtags in the first comment to keep the main caption clean.",
            "Reflect the brand's voice consistently throughout the caption.",
            "Optimize for discoverability by including relevant keywords in the first sentence.",
        ]
        return (
            prompt
            + "\n\nAdditional Instagram-specific instructions:\n"
            + "\n".join(f"- {technique}" for technique in techniques)
        )

    def generate_prompt(self, params: Dict[str, Any]) -> str:
        """Generate an optimized prompt for Instagram caption generation using an LLM."""

        tone_style_guide = self.get_tone_style_guide(params["tone"], params["style"])
        caption_size = self.get_caption_size(params["caption_length"])
        visual_description = self.generate_visual_description(params)
        hashtag_limits = self.get_hashtaglimit(params)
        influencer_persona = self.select_influencer_persona(params)
        context = self.get_context(params)

        prompt = self.template.format(
            caption_length=caption_size,
            context=context,
            content_type=params.get("content_type", "image").capitalize(),
            tone_style_guide=tone_style_guide,
            best_practices=self.platform_data["best_practices"],
            seo_tips=self.platform_data["seo_tips"],
            hashtag_limit=min(hashtag_limits, self.platform_data["hashtag_limit"]),
            max_length=self.platform_data["max_length"],
            visual_description=visual_description,
            niche=influencer_persona["niche"],
            style_description=influencer_persona["style_description"],
            content_focus=influencer_persona["content_focus"],
        )
        print(prompt)
        return self.add_prompt_engineering_techniques(prompt)
