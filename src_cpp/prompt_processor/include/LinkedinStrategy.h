#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class LinkedInStrategy : public PlatformStrategy
{
public:
    LinkedInStrategy() {}
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;
    void loadTemplate() const override;
    void loadInfluencerPersonas() const override;
    void initialize() const override;
};