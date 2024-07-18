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
    virtual std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const = 0;
    virtual void loadTemplate() const = 0;
    virtual void loadInfluencerPersonas() const = 0;
    virtual void initialize() const = 0;
};