from typing import Dict, Any
from prompt_processor.social_media_strategy import SocialMediaStrategy


class TwitterSocialMediaStrategy(SocialMediaStrategy):
    def __init__(self):
        super().__init__()

    def load_platform_data(self) -> Dict[str, Any]:
        return {
            "max_length": 280,
            "hashtag_limit": 5,
            "best_practices": "Use concise language, engage with trending topics, and leverage Twitter's real-time nature.",
            "seo_tips": "Use relevant keywords and hashtags to increase discoverability.",
            "content_types": ["TEXT", "IMAGE", "VIDEO", "GIF", "POLL"],
        }

    def load_template(self) -> str:
        with open("prompt_processor/templates/twitter_template.txt", "r") as file:
            return file.read()

    def load_influencer_personas(self) -> Dict[str, Dict[str, str]]:
        return {
            "industry_expert": {
                "niche": "current industry news",
                "style_description": "brief and impactful",
                "content_focus": "breaking news and quick insights",
            },
            "thought_leader": {
                "niche": "thought-provoking commentary",
                "style_description": "sharp and opinionated",
                "content_focus": "hot topics and trending issues",
            },
            "career_mentor": {
                "niche": "career tips and job search",
                "style_description": "concise and actionable",
                "content_focus": "quick career advice and job market updates",
            },
            "tech_innovator": {
                "niche": "latest tech trends",
                "style_description": "fast-paced and engaging",
                "content_focus": "tech breakthroughs and product updates",
            },
            "marketing_specialist": {
                "niche": "digital marketing strategies",
                "style_description": "snappy and insightful",
                "content_focus": "marketing tips and social media trends",
            },
            "financial_analyst": {
                "niche": "financial news and tips",
                "style_description": "brief and informative",
                "content_focus": "market updates and financial advice",
            },
            "brand_ambassador": {
                "niche": "brand storytelling and promotions",
                "style_description": "creative and engaging",
                "content_focus": "brand news and promotional content",
            },
            "entrepreneurial_mind": {
                "niche": "startup updates and advice",
                "style_description": "dynamic and motivational",
                "content_focus": "entrepreneurial insights and startup stories",
            },
            "pop_culture_enthusiast": {
                "niche": "trending pop culture",
                "style_description": "trendy and relatable",
                "content_focus": "pop culture trends and celebrity news",
            },
            "general": {
                "niche": "concise updates and trending topics",
                "style_description": "brief and impactful",
                "content_focus": "quick insights, news updates, and trending conversations",
            },
        }

    def add_prompt_engineering_techniques(self, prompt: str) -> str:
        """Apply prompt engineering techniques to improve LLM output for Twitter."""
        techniques = [
            "Craft a concise and attention-grabbing opening within the first 280 characters.",
            "Use strong, impactful language to convey your message efficiently.",
            "Incorporate relevant hashtags, but limit to 1-2 per tweet for best engagement.",
            "If using thread format, make sure each tweet can stand alone while contributing to the overall narrative.",
            "Include a clear call-to-action (retweet, reply, follow) when appropriate.",
            "Use Twitter-specific features like polls or Q&As to increase engagement.",
            "Mention relevant accounts to increase visibility and encourage interaction.",
            "For longer content, use the '1/x' format to indicate a thread continuation.",
            "Utilize emojis strategically to save character space and add visual interest.",
            "Consider the timing of your tweet to align with peak engagement hours for your audience.",
        ]
        return (
            prompt
            + "\n\nAdditional Twitter-specific instructions:\n"
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
            content_type=params.get("content_type", "text").capitalize(),
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
