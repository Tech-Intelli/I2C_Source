#include "FacebookStrategy.h"

// Define the array with persona information
constexpr std::array<std::pair<const char *, PersonaInfo>, 3> facebookPersonas = {{{FacebookStrategy::SOCIAL_CONNECTOR, {"community building", "friendly and engaging", "social trends and community events"}},
                                                                                   {FacebookStrategy::VISUAL_STORYTELLER, {"visual content creation", "creative and eye-catching", "image-based storytelling and carousel posts"}},
                                                                                   {FacebookStrategy::LOCAL_BUSINESS, {"local promotions", "personable and informative", "business updates and local events"}}}};

FacebookStrategy::FacebookStrategy() : PlatformPersonas<3>(facebookPersonas)
{
}

std::string
FacebookStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void FacebookStrategy::loadInfluencerPersonas() const
{
}

void FacebookStrategy::initialize()
{
    loadInfluencerPersonas();
    loadTemplate(filepath, templateData);
}
