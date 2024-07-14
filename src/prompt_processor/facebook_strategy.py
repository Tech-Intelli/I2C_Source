from typing import Dict, Any
from prompt_processor.social_media_strategy import SocialMediaStrategy


class FacebookSocialMediaStrategy(SocialMediaStrategy):
    def __init__(self):
        super().__init__()

    def load_template(self) -> str:
        with open("prompt_processor/templates/facebook_template.txt", "r") as file:
            return file.read()

    def load_platform_data(self) -> Dict[str, Any]:
        return {
            "max_length": 63206,
            "hashtag_limit": 10,
            "best_practices": "Use a mix of text, images, and videos. Encourage engagement through questions and polls.",
            "seo_tips": "Use searchable keywords in your post text and image descriptions.",
            "content_types": ["TEXT", "IMAGE", "VIDEO", "LINK", "LIVE", "STORY"],
        }

    def load_influencer_personas(self) -> Dict[str, Dict[str, str]]:
        return {
            "community_leader": {
                "niche": "community engagement and support",
                "style_description": "inclusive and supportive",
                "content_focus": "community events and support resources",
            },
            "family_lifestyle": {
                "niche": "family life and parenting",
                "style_description": "personal and relatable",
                "content_focus": "parenting tips and family stories",
            },
            "educational_instructor": {
                "niche": "educational content and workshops",
                "style_description": "informative and engaging",
                "content_focus": "educational materials and learning resources",
            },
            "business_owner": {
                "niche": "small business and entrepreneurship",
                "style_description": "practical and encouraging",
                "content_focus": "business tips and success stories",
            },
            "health_and_wellness": {
                "niche": "health advice and wellness tips",
                "style_description": "caring and motivational",
                "content_focus": "wellness tips and health updates",
            },
            "political_analyst": {
                "niche": "politics and public affairs",
                "style_description": "thoughtful and analytical",
                "content_focus": "political commentary and public policy",
            },
            "tech_enthusiast": {
                "niche": "technology trends and reviews",
                "style_description": "in-depth and current",
                "content_focus": "tech updates and gadget reviews",
            },
            "event_planner": {
                "niche": "event organization and management",
                "style_description": "detailed and organized",
                "content_focus": "event tips and planning strategies",
            },
            "personal_development": {
                "niche": "self-improvement and growth",
                "style_description": "motivational and practical",
                "content_focus": "personal development tips and success strategies",
            },
            "nonprofit": {
                "niche": "charity and social causes",
                "style_description": "passionate and community-focused",
                "content_focus": "charity events and advocacy work",
            },
            "general": {
                "niche": "professional development and networking",
                "style_description": "professional and insightful",
                "content_focus": "career tips, industry insights, and business strategies",
            },
        }

    def add_prompt_engineering_techniques(self, prompt: str) -> str:
        """Apply prompt engineering techniques to improve LLM output for Facebook."""
        techniques = [
            "Craft an attention-grabbing first sentence to appear in News Feed previews.",
            "Use a conversational tone to encourage discussion and comments.",
            "Incorporate storytelling elements to increase emotional engagement.",
            "Include relevant links with custom descriptions to drive traffic.",
            "Use Facebook-specific features like polls, events, or watch parties when appropriate.",
            "Encourage tagging and sharing to increase organic reach.",
            "Utilize line breaks and emojis to improve readability and visual appeal.",
            "Include a clear call-to-action that aligns with Facebook's algorithm (e.g., 'Comment below' rather than 'Click the link').",
            "Consider using carousel posts or albums for multiple images or extended narratives.",
            "Reflect the brand's voice consistently while adapting to Facebook's more personal environment.",
        ]
        return (
            prompt
            + "\n\nAdditional Facebook-specific instructions:\n"
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
