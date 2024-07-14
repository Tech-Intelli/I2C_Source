from typing import Dict, Any
from prompt_processor.social_media_strategy import SocialMediaStrategy


class LinkedInSocialMediaStrategy(SocialMediaStrategy):
    def __init__(self):
        super().__init__()

    def load_platform_data(self) -> Dict[str, Any]:
        return {
            "max_length": 3000,
            "hashtag_limit": 5,
            "best_practices": "Use professional language, share industry insights, and engage with your network.",
            "seo_tips": "Use relevant industry keywords and optimize your profile for search.",
            "content_types": ["TEXT", "IMAGE", "VIDEO", "ARTICLE", "DOCUMENT"],
        }

    def load_template(self) -> str:
        with open("prompt_processor/templates/linkedin_template.txt", "r") as file:
            return file.read()

    def load_influencer_personas(self) -> Dict[str, Dict[str, str]]:
        return {
            "industry_expert": {
                "niche": "industry-specific insights and trends",
                "style_description": "knowledgeable and authoritative",
                "content_focus": "detailed analysis and sector updates",
            },
            "career_coach": {
                "niche": "career advancement and job search strategies",
                "style_description": "supportive and practical",
                "content_focus": "resume tips, interview techniques, and career growth",
            },
            "executive_leader": {
                "niche": "business leadership and strategic management",
                "style_description": "strategic and visionary",
                "content_focus": "leadership strategies, company culture, and executive decision-making",
            },
            "entrepreneur": {
                "niche": "startup development and entrepreneurial advice",
                "style_description": "innovative and motivational",
                "content_focus": "startup challenges, growth strategies, and entrepreneurial success stories",
            },
            "recruitment_specialist": {
                "niche": "talent acquisition and human resources",
                "style_description": "informative and resourceful",
                "content_focus": "recruitment strategies, hiring best practices, and HR insights",
            },
            "technology_analyst": {
                "niche": "technology trends and innovations",
                "style_description": "analytical and forward-thinking",
                "content_focus": "emerging technologies, IT strategies, and tech industry developments",
            },
            "marketing_professional": {
                "niche": "marketing strategies and brand development",
                "style_description": "strategic and creative",
                "content_focus": "marketing campaigns, brand growth, and industry trends",
            },
            "product_manager": {
                "niche": "product development and management",
                "style_description": "strategic and results-oriented",
                "content_focus": "product lifecycle management, innovation, and market fit",
            },
            "business_analyst": {
                "niche": "business analysis and strategy",
                "style_description": "data-driven and strategic",
                "content_focus": "business insights, performance metrics, and strategic planning",
            },
            "legal_consultant": {
                "niche": "corporate law and legal compliance",
                "style_description": "authoritative and detail-oriented",
                "content_focus": "legal advice, compliance issues, and industry regulations",
            },
            "general": {
                "niche": "public speaking and presentation skills",
                "style_description": "engaging and impactful",
                "content_focus": "presentation techniques, speaking engagements, and communication skills",
            },
        }

    def add_prompt_engineering_techniques(self, prompt: str) -> str:
        """Apply prompt engineering techniques to improve LLM output for LinkedIn."""
        techniques = [
            "Begin with a compelling professional hook to capture attention in the feed.",
            "Use industry-specific language and terminology to demonstrate expertise.",
            "Structure content with clear headings and bullet points for easy scanning.",
            "Incorporate data, statistics, or case studies to support your points.",
            "Mention relevant LinkedIn connections or companies to increase visibility.",
            "Use LinkedIn's native content features like polls or documents when appropriate.",
            "Include a professional call-to-action that encourages meaningful engagement.",
            "Optimize for LinkedIn's algorithm by encouraging comments and discussions.",
            "Use hashtags sparingly and strategically, focusing on industry-relevant terms.",
            "Maintain a professional tone while still allowing for personality to shine through.",
        ]
        return (
            prompt
            + "\n\nAdditional LinkedIn-specific instructions:\n"
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
