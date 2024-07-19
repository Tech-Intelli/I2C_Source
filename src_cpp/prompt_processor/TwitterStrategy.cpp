#include "TwitterStrategy.h"

TwitterStrategy::TwitterStrategy()
{
    initialize();
    // template_str = std::make_unique<PromptTemplateParser>(templateData);
}

std::string TwitterStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    static thread_local std::string result;
    //  result = template_str->render(replacementsMap);
    return result;
}

void TwitterStrategy::initialize()
{
    // loadTemplate(filepath, templateData);
}
