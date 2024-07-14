from typing import Dict, Any
from prompt_processor.social_media_strategy import SocialMediaStrategy


class TikTokSocialMediaStrategy(SocialMediaStrategy):
    def __init__(self):
        super().__init__()

    def load_platform_data(self) -> Dict[str, Any]:
        return {
            "max_length": 2200,
            "hashtag_limit": 15,
            "best_practices": "Create short, engaging videos. Use trending sounds and participate in challenges.",
            "seo_tips": "Use relevant hashtags and optimize your profile for discoverability.",
            "content_types": ["VIDEO", "DUET", "STITCH", "LIVE"],
        }

    def load_template(self) -> str:
        with open("prompt_processor/templates/tiktok_template.txt", "r") as file:
            return file.read()

    def load_influencer_personas(self) -> Dict[str, Dict[str, str]]:
        return {
            "viral_creator": {
                "niche": "trending challenges and memes",
                "style_description": "fun and engaging",
                "content_focus": "viral trends and creative challenges",
            },
            "lifestyle_influencer": {
                "niche": "daily life and personal tips",
                "style_description": "relatable and entertaining",
                "content_focus": "daily routines and lifestyle hacks",
            },
            "dance_enthusiast": {
                "niche": "dance routines and choreography",
                "style_description": "energetic and visually captivating",
                "content_focus": "dance trends and original choreography",
            },
            "beauty_guru": {
                "niche": "beauty tutorials and product reviews",
                "style_description": "stylish and informative",
                "content_focus": "makeup tips and beauty hacks",
            },
            "foodie": {
                "niche": "cooking and food reviews",
                "style_description": "mouth-watering and creative",
                "content_focus": "recipes and food challenges",
            },
            "fitness_trainer": {
                "niche": "workout routines and health tips",
                "style_description": "motivational and energetic",
                "content_focus": "exercise routines and fitness tips",
            },
            "tech_reviewer": {
                "niche": "tech gadgets and reviews",
                "style_description": "trendy and informative",
                "content_focus": "product reviews and tech insights",
            },
            "travel_vlogger": {
                "niche": "travel adventures and tips",
                "style_description": "adventurous and captivating",
                "content_focus": "travel experiences and destination highlights",
            },
            "creative_artist": {
                "niche": "artistic expressions and DIY",
                "style_description": "innovative and engaging",
                "content_focus": "art projects and creative tutorials",
            },
            "general": {
                "niche": "short-form video content and trends",
                "style_description": "entertaining and creative",
                "content_focus": "viral challenges, creative videos, and engaging content",
            },
        }

    def add_prompt_engineering_techniques(self, prompt: str) -> str:
        """Apply prompt engineering techniques to improve LLM output for TikTok."""
        techniques = [
            "Create a hook in the first 3 seconds to capture viewer attention.",
            "Use trending sounds, effects, or challenges to increase discoverability.",
            "Keep the content fast-paced and dynamic to maintain viewer interest.",
            "Incorporate text overlays to emphasize key points and cater to silent viewing.",
            "Use popular TikTok transitions to make the video more engaging.",
            "Include a clear call-to-action that encourages likes, comments, or follows.",
            "Utilize trending hashtags relevant to your content and audience.",
            "Create content that encourages user participation (duets, stitches, or using your sound).",
            "Optimize your caption to include keywords and a brief, catchy description.",
            "Consider the vertical video format in your content planning and execution.",
        ]
        return (
            prompt
            + "\n\nAdditional TikTok-specific instructions:\n"
            + "\n".join(f"- {technique}" for technique in techniques)
        )

    def generate_prompt(self, params: Dict[str, Any]) -> str:
        tone_style_guide = self.get_tone_style_guide(params["tone"], params["style"])
        caption_size = self.get_caption_size(params["caption_length"])
        visual_description = self.generate_visual_description(params)
        hashtag_limits = self.get_hashtaglimit(params)
        influencer_persona = self.select_influencer_persona(params)
        context = self.get_context(params)
        prompt = self.template.format(
            caption_length=caption_size,
            context=context,
            content_type=params.get("content_type", "video").capitalize(),
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

        return self.add_prompt_engineering_techniques(prompt)
