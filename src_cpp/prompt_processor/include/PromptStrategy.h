#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <stdexcept>
#include <iostream>
#include "SocialMediaConsts.h"
#include "PlatformStrategy.h"
#include "PromptParams.h"
#include "PromptConsts.h"
#include "PlatformPersonas.h"
#include "PersonaInfo.h"
#include "personaConsts.h"
#include "Logging.h"
class PromptStrategy
{
public:
    PromptStrategy() = default;
    ~PromptStrategy() = default;
    std::string_view getPrompt(const PromptParams &params);

private:
    PlatformPersonas<35> platformPersonas;
    static constexpr std::string_view SMALL_DESC = "1 to 2 sentences";
    static constexpr std::string_view MEDIUM_DESC = "2 to 3 sentences";
    static constexpr std::string_view LARGE_DESC = "3 to 4 sentences";
    static const std::unordered_map<std::string_view, std::string_view> toneGuides;
    static const std::unordered_map<std::string_view, std::string_view> styleGuides;

    std::string getToneStyleGuide(std::string_view tone, std::string_view style) const;
    std::string_view getCaptionSize(const CaptionSize size) const;
    const std::shared_ptr<PlatformStrategy> createStrategy(SocialMedia platform);
    void createPromptMap(const PromptParams &params, std::unordered_map<std::string, std::string> &replacements);
};
