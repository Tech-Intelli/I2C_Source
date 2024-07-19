#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
#include <unordered_map>
#include <vector>
#include "PromptTemplateParser.h"
class InstagramStrategy : public PlatformStrategy
{
public:
    InstagramStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;

private:
    std::unique_ptr<PromptTemplateParser> template_str;
    std::string prompt;
    std::string templateData;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> influencerPersonas;
    static constexpr auto filepath = "../templates/insta_template.txt";
    void initialize() override;
};
