#include "PromptStrategy.h"

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

const PlatformPersonas<35> persona_info(Personas::PERSONAS_ARRAY);
std::string
PromptStrategy::getToneStyleGuide(std::string_view tone, std::string_view style) const
{
    auto toneIt = toneGuides.find(tone);
    auto styleIt = styleGuides.find(style);

    std::string_view toneGuide = (toneIt != toneGuides.end()) ? toneIt->second : "Tone not found.";
    std::string_view styleGuide = (styleIt != styleGuides.end()) ? styleIt->second : "Style not found.";

    return std::string(toneGuide) + " " + std::string(styleGuide);
}

/**
 * Returns the description of a caption size based on the given size.
 *
 * @param size The size of the caption.
 *
 * @return The description of the caption size.
 *
 * @throws std::invalid_argument If the caption size is unsupported.
 */
std::string_view
PromptStrategy::getCaptionSize(const CaptionSize size) const
{
    switch (size)
    {
    case CaptionSize::SMALL:
        return SMALL_DESC;
    case CaptionSize::MEDIUM:
        return MEDIUM_DESC;
    case CaptionSize::LARGE:
        return LARGE_DESC;
    default:
        log.error("Unsupported caption size: {} ", static_cast<int>(size));
        throw std::invalid_argument("Unsupported caption size");
    }
}
void PromptStrategy::createPromptMap(const PromptParams &params, std::unordered_map<std::string, std::string> &replacements)
{
    auto persona = platformPersonas.getPersonaInfo(params.persona);

    replacements["visual_description"] = params.visual_description;
    replacements["context"] = params.context;
    replacements["hashtag_limit"] = std::to_string(params.hashtag_limit);
    replacements["caption_size"] = getCaptionSize(params.caption_size);
    replacements["tone_style_guide"] = getToneStyleGuide(params.tone, params.style);
    replacements["caption_length"] = getCaptionSize(params.caption_size);
    replacements["content_type"] = "type";
    replacements["content_focus"] = persona ? persona->content_focus : "general";
    replacements["niche"] = persona ? persona->niche : "general";
    replacements["style_description"] = persona ? persona->style_description : "general";
}

/**
 * Creates a shared pointer to a PlatformStrategy object based on the given SocialMedia platform.
 *
 * @param platform The SocialMedia platform for which to create a PlatformStrategy object.
 *
 * @return A shared pointer to a PlatformStrategy object.
 *
 * @throws std::invalid_argument If the given platform is unsupported.
 */
const std::shared_ptr<PlatformStrategy> PromptStrategy::createStrategy(SocialMedia platform)
{
    std::string_view platformName = ToString(platform);
    return std::make_shared<PlatformStrategy>(platformName);
}

std::string_view
PromptStrategy::getPrompt(const PromptParams &params)
{
    try
    {

        std::unordered_map<std::string, std::string> replacementMap;

        auto strategy = createStrategy(params.social_media);

        createPromptMap(params, replacementMap);

        auto prompt = strategy->generatePrompt(replacementMap);
        log.info("prompt {} ", prompt);
        return prompt;
    }
    catch (const std::invalid_argument &e)
    {
        log.error("Invalid social media platform or parameter: {} ", e.what());
        return "Error: Invalid social media platform or parameter specified.";
    }
    catch (const std::out_of_range &e)
    {
        log.error("Missing required parameter: {} ", e.what());
        return "Error: Missing required parameter.";
    }
    catch (const std::exception &e)
    {
        log.error("An unexpected error occurred: {} ", e.what());
        return "Error: An unexpected error occurred. Please try again later.";
    }
}