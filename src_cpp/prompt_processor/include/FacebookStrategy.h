#pragma once
#include "PlatformStrategy.h"
#include <optional>
#include "PromptParams.h"
#include "PersonaInfo.h"
#include "platformPersonas.h"
#include "personaConsts.h"

class FacebookStrategy : public PlatformStrategy
{
public:
    FacebookStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;

private:
    void initialize() override;
    std::string templateData;
    static constexpr auto filepath = "../templates/facebook_template.txt";
};
