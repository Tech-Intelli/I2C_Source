/**
 * @file PersonaConsts.h
 * @brief Defines the Personas struct and associated constants for representing various personas.
 *
 * This file declares the `Personas` struct which includes a set of predefined personas
 * and their associated information. Each persona is characterized by a unique identifier
 * and a set of descriptive attributes encapsulated in the `PersonaInfo` struct.
 */
#pragma once

#include <string_view>
#include <array>
#include <stdexcept>
#include "PersonaInfo.h"

/**
 * @struct Personas
 * @brief Defines a collection of predefined personas and their associated details.
 *
 * The `Personas` struct provides a static collection of predefined personas, each associated with
 * a set of descriptive attributes through the `PersonaInfo` struct. This collection allows for
 * easy reference and use of common persona types within the application.
 *
 * The struct includes static constants for persona identifiers and a static array that maps
 * these identifiers to their corresponding `PersonaInfo`.
 *
 * Example usage:
 * @code
 * std::string_view persona_id = Personas::COMMUNITY_LEADER;
 * auto persona_info = Personas::PERSONAS_ARRAY[0].second; // Retrieve information for COMMUNITY_LEADER
 * @endcode
 */
struct Personas
{
    /**
     * @brief Identifier for the Community Leader persona.
     *
     * Represents a persona focused on community engagement and support.
     */
    static constexpr std::string_view COMMUNITY_LEADER = "community_leader";

    /**
     * @brief Identifier for the Family Lifestyle persona.
     *
     * Represents a persona specializing in family life and parenting.
     */
    static constexpr std::string_view FAMILY_LIFESTYLE = "family_lifestyle";

    /**
     * @brief Identifier for the Educational Instructor persona.
     *
     * Represents a persona dedicated to educational content and workshops.
     */
    static constexpr std::string_view EDUCATIONAL_INSTRUCTOR = "educational_instructor";

    /**
     * @brief Identifier for the Small Business Mentor persona.
     *
     * Represents a persona with expertise in small business and entrepreneurship.
     */
    static constexpr std::string_view SMALL_BUSINESS_MENTOR = "small_business_mentor";

    /**
     * @brief Identifier for the Health & Wellness Coach persona.
     *
     * Represents a persona offering health advice and wellness tips.
     */
    static constexpr std::string_view HEALTH_WELLNESS_COACH = "health_wellness_coach";

    /**
     * @brief Identifier for the Political Analyst persona.
     *
     * Represents a persona focused on politics and public affairs.
     */
    static constexpr std::string_view POLITICAL_ANALYST = "political_analyst";

    /**
     * @brief Identifier for the Tech Enthusiast persona.
     *
     * Represents a persona with a focus on technology trends and reviews.
     */
    static constexpr std::string_view TECH_ENTHUSIAST = "tech_enthusiast";

    /**
     * @brief Identifier for the Event Planner persona.
     *
     * Represents a persona specializing in event organization and management.
     */
    static constexpr std::string_view EVENT_PLANNER = "event_planner";

    /**
     * @brief Identifier for the Personal Development Coach persona.
     *
     * Represents a persona dedicated to self-improvement and personal growth.
     */
    static constexpr std::string_view PERSONAL_DEVELOPMENT_COACH = "personal_development_coach";

    /**
     * @brief Identifier for the Nonprofit Advocate persona.
     *
     * Represents a persona focused on charity and social causes.
     */
    static constexpr std::string_view NONPROFIT_ADVOCATE = "nonprofit_advocate";

    /**
     * @brief Identifier for the Industry Expert persona.
     *
     * Represents a persona with specialized knowledge in a particular industry.
     */
    static constexpr std::string_view INDUSTRY_EXPERT = "industry_expert";

    /**
     * @brief Identifier for the Career Mentor persona.
     *
     * Represents a persona providing career tips and job search advice.
     */
    static constexpr std::string_view CAREER_MENTOR = "career_mentor";

    /**
     * @brief Identifier for the Executive Leader persona.
     *
     * Represents a persona focused on business leadership and strategic management.
     */
    static constexpr std::string_view EXECUTIVE_LEADER = "executive_leader";

    /**
     * @brief Identifier for the Entrepreneur persona.
     *
     * Represents a persona with expertise in startup development and entrepreneurial advice.
     */
    static constexpr std::string_view ENTREPRENEUR = "entrepreneur";

    /**
     * @brief Identifier for the Financial Analyst persona.
     *
     * Represents a persona specializing in financial news and analysis.
     */
    static constexpr std::string_view FINANCIAL_ANALYST = "financial_analyst";

    /**
     * @brief Identifier for the Digital Marketing Specialist persona.
     *
     * Represents a persona with expertise in digital marketing strategies.
     */
    static constexpr std::string_view DIGITAL_MARKETING_SPECIALIST = "digital_marketing_specialist";

    /**
     * @brief Identifier for the Technology Analyst persona.
     *
     * Represents a persona focusing on technology trends and innovations.
     */
    static constexpr std::string_view TECHNOLOGY_ANALYST = "technology_analyst";

    /**
     * @brief Identifier for the Product Manager persona.
     *
     * Represents a persona involved in product development and management.
     */
    static constexpr std::string_view PRODUCT_MANAGER = "product_manager";

    /**
     * @brief Identifier for the Lifestyle Influencer persona.
     *
     * Represents a persona sharing daily life and personal tips.
     */
    static constexpr std::string_view LIFESTYLE_INFLUENCER = "lifestyle_influencer";

    /**
     * @brief Identifier for the Fitness Trainer persona.
     *
     * Represents a persona focused on workout routines and health tips.
     */
    static constexpr std::string_view FITNESS_TRAINER = "fitness_trainer";

    /**
     * @brief Identifier for the Beauty Guru persona.
     *
     * Represents a persona providing beauty tutorials and product reviews.
     */
    static constexpr std::string_view BEAUTY_GURU = "beauty_guru";

    /**
     * @brief Identifier for the Foodie persona.
     *
     * Represents a persona focused on cooking and food reviews.
     */
    static constexpr std::string_view FOODIE = "foodie";

    /**
     * @brief Identifier for the Travel Vlogger persona.
     *
     * Represents a persona sharing travel adventures and tips.
     */
    static constexpr std::string_view TRAVEL_VLOGGER = "travel_vlogger";

    /**
     * @brief Identifier for the Creative Artist persona.
     *
     * Represents a persona involved in artistic expressions and DIY projects.
     */
    static constexpr std::string_view CREATIVE_ARTIST = "creative_artist";

    /**
     * @brief Identifier for the Fashion Influencer persona.
     *
     * Represents a persona focused on fashion and personal style.
     */
    static constexpr std::string_view FASHION_INFLUENCER = "fashion_influencer";

    /**
     * @brief Identifier for the Gaming Enthusiast persona.
     *
     * Represents a persona passionate about gaming and esports.
     */
    static constexpr std::string_view GAMING_ENTHUSIAST = "gaming_enthusiast";

    /**
     * @brief Identifier for the Book Reviewer persona.
     *
     * Represents a persona specializing in literature and book reviews.
     */
    static constexpr std::string_view BOOK_REVIEWER = "book_reviewer";

    /**
     * @brief Identifier for the Music Enthusiast persona.
     *
     * Represents a persona focused on music and entertainment.
     */
    static constexpr std::string_view MUSIC_ENTHUSIAST = "music_enthusiast";

    /**
     * @brief Identifier for the Sustainability Advocate persona.
     *
     * Represents a persona focused on eco-friendly living and sustainability.
     */
    static constexpr std::string_view SUSTAINABILITY_ADVOCATE = "sustainability_advocate";

    /**
     * @brief Identifier for the Pet Care Expert persona.
     *
     * Represents a persona specializing in pet care and animal advice.
     */
    static constexpr std::string_view PET_CARE_EXPERT = "pet_care_expert";

    /**
     * @brief Identifier for the Pop Culture Enthusiast persona.
     *
     * Represents a persona focused on trending pop culture and celebrity news.
     */
    static constexpr std::string_view POP_CULTURE_ENTHUSIAST = "pop_culture_enthusiast";

    /**
     * @brief Identifier for the Personal Finance Guru persona.
     *
     * Represents a persona with expertise in personal finance and budgeting.
     */
    static constexpr std::string_view PERSONAL_FINANCE_GURU = "personal_finance_guru";

    /**
     * @brief Identifier for the Mental Health Advocate persona.
     *
     * Represents a persona focused on mental health awareness and support.
     */
    static constexpr std::string_view MENTAL_HEALTH_ADVOCATE = "mental_health_advocate";

    /**
     * @brief Identifier for the General Professional persona.
     *
     * Represents a persona involved in professional development and networking.
     */
    static constexpr std::string_view GENERAL_PROFESSIONAL = "general_professional";

    /**
     * @brief Static array mapping persona identifiers to their corresponding PersonaInfo.
     *
     * This array provides a mapping from persona identifiers to detailed persona information,
     * including niche, style description, and content focus. It serves as a centralized
     * reference for accessing persona details based on their identifier.
     *
     * The array contains 35 predefined personas, each associated with a unique identifier and
     * a set of descriptive attributes.
     */
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