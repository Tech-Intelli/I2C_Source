#include "TwitterStrategy.h"

std::string TwitterStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void TwitterStrategy::initialize()
{
    loadTemplate(filepath, templateData);
}
