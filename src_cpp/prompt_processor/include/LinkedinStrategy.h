#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class LinkedInStrategy : public PlatformStrategy
{
public:
    LinkedInStrategy() {}
    std::string_view generatePrompt(const PromptParams &params) const override;
    std::unordered_map<std::string, std::string> loadPlatformData() const override;
    std::string_view loadTemplate() const override;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> loadInfluencerPersonas() const override;
    std::string addPromptEngineeringTechniques(const std::string &prompt) const override;
};