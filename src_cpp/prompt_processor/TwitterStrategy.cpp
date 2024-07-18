#include "TwitterStrategy.h"

std::string TwitterStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void TwitterStrategy::loadTemplate() const
{
}

void TwitterStrategy::loadInfluencerPersonas() const
{
}

void TwitterStrategy::initialize() const
{
    loadInfluencerPersonas();
    loadTemplate();
}
