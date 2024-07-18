#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class TwitterStrategy : public PlatformStrategy
{
public:
    TwitterStrategy() {}
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;
    void loadTemplate() const override;
    void loadInfluencerPersonas() const override;
    void initialize() const override;
    void createPromptMap(const PromptParams &params, std::unordered_map<std::string, std::string> &replacements) override;
};