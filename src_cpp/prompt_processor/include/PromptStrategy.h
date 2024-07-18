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
#include "PromptParams.h"
#include "PromptConsts.h"
#include "Logging.h"
class PromptStrategy
{
public:
    PromptStrategy() = default;
    ~PromptStrategy() = default;

    const std::shared_ptr<PlatformStrategy> createStrategy(SocialMedia platform);
    std::string_view getPrompt(const PromptParams &params);

private:
    static constexpr std::string_view SMALL_DESC = "1 to 2 sentences";
    static constexpr std::string_view MEDIUM_DESC = "2 to 3 sentences";
    static constexpr std::string_view LARGE_DESC = "4 to 5 sentences";
    static const std::unordered_map<std::string_view, std::string_view> toneGuides;
    static const std::unordered_map<std::string_view, std::string_view> styleGuides;

    std::tuple<std::string_view, std::string_view> getToneStyleGuide(std::string_view tone, std::string_view style) const;
    std::unordered_map<std::string, std::string> selectInfluencerPersona(const PromptParams &params) const;
    std::string_view getVisualDescription(const PromptParams &params) const;
    std::string_view getContext(const PromptParams &params) const;
    int getHashtagLimit(const PromptParams &params) const;
    std::string_view getCaptionSize(const CaptionSize size) const;
};
