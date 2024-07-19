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
    static constexpr auto filepath = "../templates/insta_template.txt";
    void initialize() override;
};
