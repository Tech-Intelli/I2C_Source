#include "LinkedinStrategy.h"

std::string
LinkedInStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void LinkedInStrategy::initialize()
{
    loadTemplate(filepath, templateData);
}
