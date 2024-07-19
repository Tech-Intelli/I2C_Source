#include "FacebookStrategy.h"

// Define the array with persona information

FacebookStrategy::FacebookStrategy()
{
}

std::string
FacebookStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    return std::string();
}

void FacebookStrategy::initialize()
{
    loadTemplate(filepath, templateData);
}
