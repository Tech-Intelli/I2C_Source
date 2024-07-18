#include "InstagramStrategy.h"

InstagramStrategy::InstagramStrategy()
{
    initialize();
    template_str = std::make_unique<StringTemplate>(templateData);
}

std::string
InstagramStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    static thread_local std::string result;
    result = template_str->render(replacementsMap);
    return result;
}

void InstagramStrategy::loadTemplate() const
{
}

void InstagramStrategy::loadInfluencerPersonas() const
{
}

void InstagramStrategy::initialize() const
{
    loadInfluencerPersonas();
    loadTemplate();
}

void InstagramStrategy::createPromptMap(const PromptParams &params, std::unordered_map<std::string, std::string> &replacements)
{
    replacements["visual_description"] = params.visual_description;
    replacements["context"] = params.context;
    replacements["hashtag_limit"] = std::to_string(params.hashtag_limit);
}
