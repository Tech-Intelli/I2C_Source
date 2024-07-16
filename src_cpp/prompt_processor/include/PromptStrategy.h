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

class PromptStrategy
{
public:
    PromptStrategy();
    virtual ~PromptStrategy() = default;

    virtual std::tuple<std::string_view, std::string_view> getToneStyleGuide(std::string_view tone, std::string_view style) const;
    virtual std::unordered_map<std::string, std::string> selectInfluencerPersona(const PromptParams &params) const;
    virtual std::string_view generateVisualDescription(const PromptParams &params) const;
    virtual std::string_view getContext(const PromptParams &params) const;
    virtual int getHashtagLimit(const PromptParams &params) const;
    virtual std::string_view getCaptionSize(const CaptionSize size) const;
    virtual const std::shared_ptr<PlatformStrategy> createStrategy(SocialMedia platform);
    virtual std::string_view getPrompt(const PromptParams &params);

private:
    static const std::unordered_map<std::string_view, std::string_view> toneGuides;
    static const std::unordered_map<std::string_view, std::string_view> styleGuides;
};
constexpr std::string_view SMALL_DESC = "1 to 2 sentences";
constexpr std::string_view MEDIUM_DESC = "2 to 3 sentences";
constexpr std::string_view LARGE_DESC = "4 to 5 sentences";
