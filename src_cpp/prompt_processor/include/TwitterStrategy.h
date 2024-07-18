#pragma once

#include "PlatformStrategy.h"
#include "PromptParams.h"
class TwitterStrategy : public PlatformStrategy
{
public:
    TwitterStrategy() {}
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;
    void loadInfluencerPersonas() const override;
    void initialize() override;

private:
    static constexpr auto filepath = "../templates/twitter_template.txt";
};