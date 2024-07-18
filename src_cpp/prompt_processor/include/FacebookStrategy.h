#pragma once
#include "PlatformStrategy.h"
#include <optional>
#include "PromptParams.h"
#include "PersonaInfo.h"
#include "platformPersonas.h"
#include "personaConsts.h"

class FacebookStrategy : public PlatformStrategy, public PlatformPersonas<35>
{
public:
    FacebookStrategy();
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;
    void loadInfluencerPersonas() const override;
    void initialize() override;

private:
    static constexpr auto filepath = "../templates/facebook_template.txt";
};
