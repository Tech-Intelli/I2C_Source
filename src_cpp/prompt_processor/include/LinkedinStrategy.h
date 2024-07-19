#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class LinkedInStrategy : public PlatformStrategy
{
public:
    LinkedInStrategy() {}
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;

private:
    void initialize() override;
    std::string templateData;
    static constexpr auto filepath = "../templates/linkedin_template.txt";
};