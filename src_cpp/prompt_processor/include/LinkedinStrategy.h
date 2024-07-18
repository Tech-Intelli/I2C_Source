#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class LinkedInStrategy : public PlatformStrategy
{
public:
    LinkedInStrategy() {}
    std::string generatePrompt(const PromptParams &params) const override;
    void loadPlatformData() const override;
    void loadTemplate() const override;
    void loadInfluencerPersonas() const override;
    void loadPromptEngineeringTechniques(const std::string &prompt) const override;
};