#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
#include <unordered_map>
#include <vector>
class InstagramStrategy : public PlatformStrategy
{
public:
    InstagramStrategy();
    std::string generatePrompt(const PromptParams &params) const override;
    void loadPlatformData() const override;
    void loadTemplate() const override;
    void loadInfluencerPersonas() const override;
    void loadPromptEngineeringTechniques() const override;
    void initialize() const override;

private:
    std::string prompt;
    std::string templateData;
    std::unordered_map<std::string, std::string> platformData;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> influencerPersonas;
    std::vector<std::string> promptEngineeringTechniques;
};
