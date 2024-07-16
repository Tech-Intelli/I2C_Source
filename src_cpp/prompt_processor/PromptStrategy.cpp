#include "PromptStrategy.h"

// Static member definitions
const std::unordered_map<std::string_view, std::string_view> PromptStrategy::toneGuides = {
    {"casual", "Use conversational language and a friendly approach."},
    {"professional", "Maintain a polished and authoritative voice."},
    {"humorous", "Incorporate wit and levity, but ensure it's appropriate for the audience."},
    {"inspirational", "Use uplifting language and motivational phrases."},
    {"educational", "Present information clearly and concisely, focusing on key takeaways."},
    {"empathetic", "Show understanding and compassion for your audience's experiences."},
    {"enthusiastic", "Express excitement and passion about the topic."},
    {"formal", "Use proper language and maintain a serious, business-like tone."},
    {"sarcastic", "Use irony and wit, but be cautious not to offend."},
    {"nostalgic", "Evoke fond memories and emotions from the past."}};

const std::unordered_map<std::string_view, std::string_view> PromptStrategy::styleGuides = {
    {"informative", "Prioritize facts and valuable insights."},
    {"storytelling", "Weave a narrative that captures attention and relates to the audience."},
    {"persuasive", "Use compelling arguments and calls-to-action."},
    {"descriptive", "Paint a vivid picture with words, emphasizing sensory details."},
    {"minimalist", "Keep it simple and straightforward, focusing on essential elements."},
    {"comparative", "Highlight differences and similarities between concepts or products."},
    {"how-to", "Provide step-by-step instructions or tutorials."},
    {"listicle", "Present information in an easily digestible numbered or bulleted list format."},
    {"behind-the-scenes", "Offer exclusive looks into processes, people, or places."},
    {"trending", "Capitalize on current events, popular topics, and viral content in your niche."}};

PromptStrategy::PromptStrategy()
{
}

std::tuple<std::string_view, std::string_view>
PromptStrategy::getToneStyleGuide(std::string_view tone, std::string_view style) const
{
    auto toneIt = toneGuides.find(tone);
    auto styleIt = styleGuides.find(style);

    std::string_view toneGuide = (toneIt != toneGuides.end()) ? toneIt->second : "Tone not found.";
    std::string_view styleGuide = (styleIt != styleGuides.end()) ? styleIt->second : "Style not found.";

    return std::make_tuple(toneGuide, styleGuide);
}

std::unordered_map<std::string, std::string>
PromptStrategy::selectInfluencerPersona(const std::unordered_map<std::string, std::string> &params) const
{
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> personas;

    return personas.at("general");
}

std::string
PromptStrategy::generateVisualDescription(const std::unordered_map<std::string, std::string> &params) const
{
    return params.at("visual_description");
}

std::string
PromptStrategy::getContext(const std::unordered_map<std::string, std::string> &params) const
{
    return params.at("context");
}

std::string
PromptStrategy::getHashtagLimit(const std::unordered_map<std::string, std::string> &params) const
{
    return params.at("hashtag_limit");
}

std::string
PromptStrategy::getCaptionSize(const std::string &captionSize) const
{
    static const std::unordered_map<std::string, std::string> captionLengthMapping = {
        {"small", "1 to 2 sentences"},
        {"medium", "2 to 3 sentences"},
        {"large", "4 to 5 sentences"}};

    return captionLengthMapping.at(captionSize);
}

const std::shared_ptr<PlatformStrategy> PromptStrategy::createStrategy(SocialMedia platform)
{
    switch (platform)
    {
    case SocialMedia::INSTAGRAM:
        return std::make_shared<InstagramStrategy>();
    case SocialMedia::TWITTER:
        return std::make_shared<TwitterStrategy>();
    case SocialMedia::LINKEDIN:
        return std::make_shared<LinkedInStrategy>();
    case SocialMedia::FACEBOOK:
        return std::make_shared<FacebookStrategy>();
    case SocialMedia::TIKTOK:
        return std::make_shared<TiktokStrategy>();
    default:
        std::cerr << "Unsupported platform: " << static_cast<int>(platform) << std::endl;
        throw std::invalid_argument("Unsupported social media platform");
    }
}

std::string
PromptStrategy::getPrompt(const std::unordered_map<std::string, std::string> &params)
{
    try
    {
        // Convert string to SocialMedia enum
        SocialMedia socialMedia = FromString(params.at("social_media"));
        auto strategy = createStrategy(socialMedia);
        std::string prompt = strategy->generatePrompt(params);
        return prompt;
    }
    catch (const std::invalid_argument &e)
    {
        std::cerr << "Invalid social media platform or parameter: " << e.what() << std::endl;
        return "Error: Invalid social media platform or parameter specified.";
    }
    catch (const std::out_of_range &e)
    {
        std::cerr << "Missing required parameter: " << e.what() << std::endl;
        return "Error: Missing required parameter.";
    }
    catch (const std::exception &e)
    {
        std::cerr << "An unexpected error occurred: " << e.what() << std::endl;
        return "Error: An unexpected error occurred. Please try again later.";
    }
}