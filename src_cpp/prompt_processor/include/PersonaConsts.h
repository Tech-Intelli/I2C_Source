#include <string_view>
#include <array>
#include <stdexcept>
#include "PersonaInfo.h"

struct Personas
{
    static constexpr std::string_view COMMUNITY_LEADER = "community_leader";
    static constexpr std::string_view FAMILY_LIFESTYLE = "family_lifestyle";
    static constexpr std::string_view EDUCATIONAL_INSTRUCTOR = "educational_instructor";
    static constexpr std::string_view SMALL_BUSINESS_MENTOR = "small_business_mentor";
    static constexpr std::string_view HEALTH_WELLNESS_COACH = "health_wellness_coach";
    static constexpr std::string_view POLITICAL_ANALYST = "political_analyst";
    static constexpr std::string_view TECH_ENTHUSIAST = "tech_enthusiast";
    static constexpr std::string_view EVENT_PLANNER = "event_planner";
    static constexpr std::string_view PERSONAL_DEVELOPMENT_COACH = "personal_development_coach";
    static constexpr std::string_view NONPROFIT_ADVOCATE = "nonprofit_advocate";
    static constexpr std::string_view INDUSTRY_EXPERT = "industry_expert";
    static constexpr std::string_view CAREER_MENTOR = "career_mentor";
    static constexpr std::string_view EXECUTIVE_LEADER = "executive_leader";
    static constexpr std::string_view ENTREPRENEUR = "entrepreneur";
    static constexpr std::string_view FINANCIAL_ANALYST = "financial_analyst";
    static constexpr std::string_view DIGITAL_MARKETING_SPECIALIST = "digital_marketing_specialist";
    static constexpr std::string_view TECHNOLOGY_ANALYST = "technology_analyst";
    static constexpr std::string_view PRODUCT_MANAGER = "product_manager";
    static constexpr std::string_view LIFESTYLE_INFLUENCER = "lifestyle_influencer";
    static constexpr std::string_view FITNESS_TRAINER = "fitness_trainer";
    static constexpr std::string_view BEAUTY_GURU = "beauty_guru";
    static constexpr std::string_view FOODIE = "foodie";
    static constexpr std::string_view TRAVEL_VLOGGER = "travel_vlogger";
    static constexpr std::string_view CREATIVE_ARTIST = "creative_artist";
    static constexpr std::string_view FASHION_INFLUENCER = "fashion_influencer";
    static constexpr std::string_view GAMING_ENTHUSIAST = "gaming_enthusiast";
    static constexpr std::string_view BOOK_REVIEWER = "book_reviewer";
    static constexpr std::string_view MUSIC_ENTHUSIAST = "music_enthusiast";
    static constexpr std::string_view SUSTAINABILITY_ADVOCATE = "sustainability_advocate";
    static constexpr std::string_view PET_CARE_EXPERT = "pet_care_expert";
    static constexpr std::string_view POP_CULTURE_ENTHUSIAST = "pop_culture_enthusiast";
    static constexpr std::string_view PERSONAL_FINANCE_GURU = "personal_finance_guru";
    static constexpr std::string_view MENTAL_HEALTH_ADVOCATE = "mental_health_advocate";
    static constexpr std::string_view GENERAL_PROFESSIONAL = "general_professional";

    static constexpr std::array<std::pair<const std::string_view, PersonaInfo>, 35> PERSONAS_ARRAY = {{{Personas::COMMUNITY_LEADER, {"community engagement and support", "inclusive and supportive", "community events and support resources"}},
                                                                                                       {Personas::FAMILY_LIFESTYLE, {"family life and parenting", "personal and relatable", "parenting tips and family stories"}},
                                                                                                       {Personas::EDUCATIONAL_INSTRUCTOR, {"educational content and workshops", "informative and engaging", "educational materials and learning resources"}},
                                                                                                       {Personas::SMALL_BUSINESS_MENTOR, {"small business and entrepreneurship", "practical and encouraging", "business tips and success stories"}},
                                                                                                       {Personas::HEALTH_WELLNESS_COACH, {"health advice and wellness tips", "caring and motivational", "wellness tips and health updates"}},
                                                                                                       {Personas::POLITICAL_ANALYST, {"politics and public affairs", "thoughtful and analytical", "political commentary and public policy"}},
                                                                                                       {Personas::TECH_ENTHUSIAST, {"technology trends and reviews", "in-depth and current", "tech updates and gadget reviews"}},
                                                                                                       {Personas::EVENT_PLANNER, {"event organization and management", "detailed and organized", "event tips and planning strategies"}},
                                                                                                       {Personas::PERSONAL_DEVELOPMENT_COACH, {"self-improvement and growth", "motivational and practical", "personal development tips and success strategies"}},
                                                                                                       {Personas::NONPROFIT_ADVOCATE, {"charity and social causes", "passionate and community-focused", "charity events and advocacy work"}},
                                                                                                       {Personas::INDUSTRY_EXPERT, {"industry-specific insights and trends", "knowledgeable and authoritative", "detailed analysis and sector updates"}},
                                                                                                       {Personas::CAREER_MENTOR, {"career tips and job search", "concise and actionable", "quick career advice and job market updates"}},
                                                                                                       {Personas::EXECUTIVE_LEADER, {"business leadership and strategic management", "strategic and visionary", "leadership strategies, company culture, and executive decision-making"}},
                                                                                                       {Personas::ENTREPRENEUR, {"startup development and entrepreneurial advice", "innovative and motivational", "startup challenges, growth strategies, and success stories"}},
                                                                                                       {Personas::FINANCIAL_ANALYST, {"financial news and tips", "brief and informative", "market updates and financial advice"}},
                                                                                                       {Personas::DIGITAL_MARKETING_SPECIALIST, {"digital marketing strategies", "snappy and insightful", "marketing tips and social media trends"}},
                                                                                                       {Personas::TECHNOLOGY_ANALYST, {"technology trends and innovations", "analytical and forward-thinking", "emerging technologies, IT strategies, and tech industry developments"}},
                                                                                                       {Personas::PRODUCT_MANAGER, {"product development and management", "strategic and results-oriented", "product lifecycle management, innovation, and market fit"}},
                                                                                                       {Personas::LIFESTYLE_INFLUENCER, {"daily life and personal tips", "relatable and entertaining", "daily routines and lifestyle hacks"}},
                                                                                                       {Personas::FITNESS_TRAINER, {"workout routines and health tips", "motivational and energetic", "exercise routines and fitness tips"}},
                                                                                                       {Personas::BEAUTY_GURU, {"beauty tutorials and product reviews", "stylish and informative", "makeup tips and beauty hacks"}},
                                                                                                       {Personas::FOODIE, {"cooking and food reviews", "mouth-watering and creative", "recipes and food challenges"}},
                                                                                                       {Personas::TRAVEL_VLOGGER, {"travel adventures and tips", "adventurous and captivating", "travel experiences and destination highlights"}},
                                                                                                       {Personas::CREATIVE_ARTIST, {"artistic expressions and DIY", "innovative and engaging", "art projects and creative tutorials"}},
                                                                                                       {Personas::FASHION_INFLUENCER, {"fashion and personal style", "trendy and expressive", "outfit inspiration and fashion tips"}},
                                                                                                       {Personas::GAMING_ENTHUSIAST, {"gaming and esports", "enthusiastic and entertaining", "game reviews and streaming highlights"}},
                                                                                                       {Personas::BOOK_REVIEWER, {"literature and book reviews", "thoughtful and analytical", "book recommendations and reading challenges"}},
                                                                                                       {Personas::MUSIC_ENTHUSIAST, {"music and entertainment", "upbeat and trend-setting", "music reviews and artist spotlights"}},
                                                                                                       {Personas::SUSTAINABILITY_ADVOCATE, {"eco-friendly living and sustainability", "environmentally conscious and informative", "eco-tips and sustainable product reviews"}},
                                                                                                       {Personas::PET_CARE_EXPERT, {"pet care and animal lovers", "warm and educational", "pet care advice and cute animal content"}},
                                                                                                       {Personas::POP_CULTURE_ENTHUSIAST, {"trending pop culture", "trendy and relatable", "pop culture trends and celebrity news"}},
                                                                                                       {Personas::PERSONAL_FINANCE_GURU, {"personal finance and budgeting", "practical and informative", "saving tips, budgeting strategies, and financial planning"}},
                                                                                                       {Personas::MENTAL_HEALTH_ADVOCATE, {"mental health awareness and support", "empathetic and supportive", "mental health tips, coping strategies, and personal stories"}},
                                                                                                       {Personas::GENERAL_PROFESSIONAL, {"professional development and networking", "professional and insightful", "career tips, industry insights, and business strategies"}}}};
};