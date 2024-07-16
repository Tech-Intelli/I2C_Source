#pragma once

#include <string>
#include <unordered_map>
#include <memory>

// Abstract base class for BasePlatformStrategy
class PlatformStrategy
{
public:
    virtual ~PlatformStrategy() = default;
    PlatformStrategy();

    virtual std::string generatePrompt(const std::unordered_map<std::string, std::string> &params) const = 0;
    virtual std::unordered_map<std::string, std::string> loadPlatformData() const = 0;
    virtual std::string_view loadTemplate() const = 0;
    virtual std::unordered_map<std::string, std::unordered_map<std::string, std::string>> loadInfluencerPersonas() const = 0;
    virtual std::string addPromptEngineeringTechniques(const std::string &prompt) const = 0;

    void initialize();

    std::unordered_map<std::string, std::string> platformData;
    std::string_view templateData;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> influencerPersonas;
};