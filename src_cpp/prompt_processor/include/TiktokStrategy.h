#pragma once

#include "PlatformStrategy.h"

class TiktokStrategy : public PlatformStrategy

{
public:
    TiktokStrategy() {}
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &params) const override;
    std::unordered_map<std::string, std::string> loadPlatformData() const override;
    std::string_view loadTemplate() const override;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> loadInfluencerPersonas() const override;
    std::string addPromptEngineeringTechniques(const std::string &prompt) const override;
};