#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
#include <unordered_map>
#include <vector>
#include "StringTemplate.h"
class InstagramStrategy : public PlatformStrategy
{
public:
    InstagramStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;
    void loadTemplate() const override;
    void loadInfluencerPersonas() const override;
    void initialize() const override;

private:
    std::unique_ptr<StringTemplate> template_str;
    std::string prompt;
    std::string templateData;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> influencerPersonas;
};
