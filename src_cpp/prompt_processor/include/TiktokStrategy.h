#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
#include "PromptTemplateParser.h"

class TiktokStrategy

{
public:
    TiktokStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const;

private:
    static constexpr auto filepath = "../templates/tiktok_template.txt";
    void initialize();
};