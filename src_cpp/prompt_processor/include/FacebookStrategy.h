#pragma once
#include "PlatformStrategy.h"
#include <optional>
#include "PromptParams.h"
#include "PersonaInfo.h"
#include "platformPersonas.h"

class FacebookStrategy : public PlatformStrategy, public PlatformPersonas<3>
{
public:
    static constexpr const char *SOCIAL_CONNECTOR = "social_connector";
    static constexpr const char *VISUAL_STORYTELLER = "visual_storyteller";
    static constexpr const char *LOCAL_BUSINESS = "local_business";
    // Constructor initializes PlatformPersonas<3> with the persona data
    FacebookStrategy();

    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap) const override;
    void loadInfluencerPersonas() const override;
    void initialize() override;

private:
    static constexpr auto filepath = "../templates/facebook_template.txt";
};
