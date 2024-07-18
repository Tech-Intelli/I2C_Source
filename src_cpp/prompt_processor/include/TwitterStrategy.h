#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class TwitterStrategy : public PlatformStrategy
{
public:
    TwitterStrategy() {}
    std::string generatePrompt(const PromptParams &params) const override;
    void loadPlatformData() const override;
    void loadTemplate() const override;
    void loadInfluencerPersonas() const override;
    void loadPromptEngineeringTechniques() const override;
    void initialize() const override;
};