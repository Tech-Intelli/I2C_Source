#include "FacebookStrategy.h"

// Define the array with persona information

FacebookStrategy::FacebookStrategy() : PlatformPersonas<35>(Personas::PERSONAS_ARRAY)
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
