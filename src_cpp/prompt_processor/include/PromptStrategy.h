#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <stdexcept>
#include <iostream>
#include "SocialMediaConsts.h"
#include "InstagramStrategy.h"
#include "TwitterStrategy.h"
#include "LinkedinStrategy.h"
#include "FacebookStrategy.h"
#include "TiktokStrategy.h"
#include "PlatformStrategy.h"

// Abstract base class for social media strategy
class PromptStrategy
{
public:
    PromptStrategy();
    virtual ~PromptStrategy() = default;

    virtual std::tuple<std::string_view, std::string_view> getToneStyleGuide(std::string_view tone, std::string_view style) const;
    virtual std::unordered_map<std::string, std::string> selectInfluencerPersona(const std::unordered_map<std::string, std::string> &params) const;
    virtual std::string generateVisualDescription(const std::unordered_map<std::string, std::string> &params) const;
    virtual std::string getContext(const std::unordered_map<std::string, std::string> &params) const;
    virtual std::string getHashtagLimit(const std::unordered_map<std::string, std::string> &params) const;
    virtual std::string getCaptionSize(const std::string &captionSize = "small") const;
    virtual const std::shared_ptr<PlatformStrategy> createStrategy(SocialMedia platform);
    virtual std::string getPrompt(const std::unordered_map<std::string, std::string> &params);

private:
    static const std::unordered_map<std::string_view, std::string_view> toneGuides;
    static const std::unordered_map<std::string_view, std::string_view> styleGuides;
};
