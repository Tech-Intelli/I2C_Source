#include "TiktokStrategy.h"

std::string TiktokStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void TiktokStrategy::loadTemplate() const
{
}

void TiktokStrategy::loadInfluencerPersonas() const
{
}

void TiktokStrategy::initialize() const
{
    loadInfluencerPersonas();
    loadTemplate();
}

void TiktokStrategy::createPromptMap(const PromptParams &params, std::unordered_map<std::string, std::string> &replacements)
{
}
