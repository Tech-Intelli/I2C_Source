#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
#include "PromptTemplateParser.h"

class LinkedInStrategy : public PlatformStrategy
{
public:
    LinkedInStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;

private:
    static constexpr auto filepath = "../templates/linkedin_template.txt";
    void initialize() override;
};