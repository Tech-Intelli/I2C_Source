#include "TiktokStrategy.h"

std::string TiktokStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void TiktokStrategy::loadInfluencerPersonas() const
{
}

void TiktokStrategy::initialize()
{
    loadInfluencerPersonas();
    loadTemplate(filepath, templateData);
}
