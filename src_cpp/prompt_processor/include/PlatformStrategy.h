#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include "PromptParams.h"

class PlatformStrategy
{
public:
    virtual ~PlatformStrategy() = default;
    PlatformStrategy() = default;
    virtual std::string generatePrompt(const PromptParams &params) const = 0;
    virtual void loadPlatformData() const = 0;
    virtual void loadTemplate() const = 0;
    virtual void loadInfluencerPersonas() const = 0;
    virtual void loadPromptEngineeringTechniques(const std::string &prompt) const = 0;
};