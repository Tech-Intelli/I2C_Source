#include "TiktokStrategy.h"

TiktokStrategy::TiktokStrategy()
{
    initialize();
    // template_str = std::make_unique<PromptTemplateParser>(templateData);
}

std::string TiktokStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    static thread_local std::string result;
    // result = template_str->render(replacementsMap);
    return result;
}

void TiktokStrategy::initialize()
{

    // loadTemplate(filepath, templateData);
}
