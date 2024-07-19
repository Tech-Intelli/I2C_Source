#include <iostream>
#include <string_view>
#include "Logging.h"
#include "SocialMediaConsts.h"
#include "PromptStrategy.h"
#include "PlatformPersonas.h"
#include "PersonaConsts.h"

int main()
{
    Log::init();
    SocialMedia platform = SocialMedia::INSTAGRAM;
    std::string_view platformName = ToString(platform);
    log.info("Enum to string: {} ", platformName);

    try
    {
        std::string_view platformName = "twitter";
        SocialMedia platformEnum = FromString(platformName);
        log.info("String to enum: {} ", static_cast<int>(platformEnum));
    }
    catch (const std::invalid_argument &e)
    {
        log.error("Error: {} ", e.what());
    }

    try
    {
        std::string_view invalidPlatformName = "myspace";
        SocialMedia invalidPlatformEnum = FromString(invalidPlatformName);
        log.debug("String to enum: {} ", static_cast<int>(invalidPlatformEnum));
    }
    catch (const std::invalid_argument &e)
    {
        log.error("Error: {} ", e.what());
    }
    PlatformPersonas<35> persona_info(Personas::PERSONAS_ARRAY);
    auto persona = persona_info.getPersonaInfo(Personas::COMMUNITY_LEADER);
    if (persona)
    {
        log.info("content focus: {} ", persona->content_focus);
        log.info("niche: {} ", persona->niche);
        log.info("style description: {} ", persona->style_description);
    }
    PromptStrategy prompt;

    PromptParams params = PromptParams(SocialMedia::INSTAGRAM, // social media platform to use
                                       "visual description",   // visual description of the content
                                       "context",              // context of the content
                                       3,                      // limit on the number of hashtags to include in the prompt
                                       CaptionSize::SMALL,     // caption size
                                       "tone",                 // tone of the content
                                       "style",
                                       Personas::BEAUTY_GURU // style of the content
    );
    prompt.getPrompt(params);

    return 0;
}
