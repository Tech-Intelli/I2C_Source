#include "InstagramStrategy.h"

InstagramStrategy::InstagramStrategy()
{
    initialize();
    template_str = std::make_unique<PromptTemplateParser>(templateData);
}

std::string
InstagramStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    static thread_local std::string result;
    result = template_str->render(replacementsMap);
    return result;
}

void InstagramStrategy::loadInfluencerPersonas() const
{
}

void InstagramStrategy::initialize()
{
    loadInfluencerPersonas();
    loadTemplate(filepath, templateData);
}
