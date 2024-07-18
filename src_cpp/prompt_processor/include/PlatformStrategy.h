#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <fstream>
#include "PromptParams.h"

class PlatformStrategy
{
public:
    virtual ~PlatformStrategy() = default;
    PlatformStrategy() = default;
    virtual std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const = 0;
    void loadTemplate(const std::string &file_path, std::string &templateData);
    virtual void loadInfluencerPersonas() const = 0;
    virtual void initialize() = 0;
    std::string templateData;
};