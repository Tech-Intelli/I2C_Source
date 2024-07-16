#include "LinkedinStrategy.h"

std::string_view LinkedInStrategy::generatePrompt(const PromptParams &params) const
{
    return std::string_view();
}

std::unordered_map<std::string, std::string> LinkedInStrategy::loadPlatformData() const
{
    return std::unordered_map<std::string, std::string>();
}

std::string_view LinkedInStrategy::loadTemplate() const
{
    return std::string_view();
}

std::unordered_map<std::string, std::unordered_map<std::string, std::string>> LinkedInStrategy::loadInfluencerPersonas() const
{
    return std::unordered_map<std::string, std::unordered_map<std::string, std::string>>();
}

std::string LinkedInStrategy::addPromptEngineeringTechniques(const std::string &prompt) const
{
    return std::string();
}
