#pragma once

#include "PlatformStrategy.h"
#include <optional>
#include "PromptParams.h"
#include "PersonaInfo.h"
#include "platformPersonas.h"
#include "personaConsts.h"
#include "PromptTemplateParser.h"

class FacebookStrategy : public PlatformStrategy
{
public:
    FacebookStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;

private:
    static constexpr auto filepath = "../templates/facebook_template.txt";
    void initialize() override;
};
