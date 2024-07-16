#include "TiktokStrategy.h"

std::string_view TiktokStrategy::generatePrompt(const PromptParams &params) const
{
    return std::string();
}

std::unordered_map<std::string, std::string> TiktokStrategy::loadPlatformData() const
{
    return std::unordered_map<std::string, std::string>();
}

std::string_view TiktokStrategy::loadTemplate() const
{
    return std::string_view();
}

std::unordered_map<std::string, std::unordered_map<std::string, std::string>> TiktokStrategy::loadInfluencerPersonas() const
{
    return std::unordered_map<std::string, std::unordered_map<std::string, std::string>>();
}

std::string TiktokStrategy::addPromptEngineeringTechniques(const std::string &prompt) const
{
    return std::string();
}
