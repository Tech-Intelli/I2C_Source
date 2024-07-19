#include "FacebookStrategy.h"

// Define the array with persona information

FacebookStrategy::FacebookStrategy()
{
    initialize();
    //  template_str = std::make_unique<PromptTemplateParser>(templateData);
}

std::string
FacebookStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const
{
    static thread_local std::string result;
    // result = template_str->render(replacementsMap);
    return result;
}

void FacebookStrategy::initialize()
{
    // loadTemplate(filepath, templateData);
}
